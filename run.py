#!/usr/bin/env python
'''
Usage: run.py [ options ]

DJDNS Hyperboria Hosting

For security, this script uses privelege dropping to host on port 53 without
running as root during regular operation. You start the script as root, and
provide it with a user and group to drop to. Make sure these are allowed to
read the data files in DIR.

Options:
    -h --help  Show this message
    -d DIR     Root directory for domain information [default: .]
    -u USER    User to run as during regular operation  [default: nobody]
    -g GROUP   Group to run as during regular operation [default: nobody]
'''

from docopt import docopt
import os
import grp
import pwd
import threading
import traceback

from djdns.server import DJServer

def get_uid(username):
    return pwd.getpwnam(username).pw_uid

def get_gid(groupname):
    return grp.getgrnam(groupname).gr_gid

def drop_priveleges(user, group):
    uid = get_uid(user)
    gid = get_gid(group)
    os.setgid(gid)
    os.setuid(uid)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1')
    os.chdir(arguments['-d'])
    config_ipv4 = {
        'listen_host': '0.0.0.0',
        'listen_port': 53,
        'path' : './root.json',
    }
    server_ipv4 = DJServer(**config_ipv4)
    server_ipv4.bind()
    try:
        drop_priveleges(arguments['-u'], arguments['-g'])
    except:
        traceback.print_exc()
        server_ipv4.stop()

    thread_ipv4 = threading.Thread(target=server_ipv4.serve)
    thread_ipv4.daemon = True
    thread_ipv4.start()

    while server_ipv4.serving:
        try:
            thread_ipv4.join(1)
        except KeyboardInterrupt:
            print "STOPPING SERVER"
            server_ipv4.stop()
    thread_ipv4.join(1)
