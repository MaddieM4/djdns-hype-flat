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
import time
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

def serve_threaded(server):
    thread = threading.Thread(target=server.serve)
    thread.daemon = True
    thread.start()
    return thread

def serve_wait(*servers):
    try:
        while True:
            time.sleep(1)
            for server in servers:
                if not server.serving:
                    break
    except KeyboardInterrupt:
        pass

    for server in servers:
        print "STOPPING SERVER %r" % server
        server.stop()
        server.thread.join(1)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1')
    os.chdir(arguments['-d'])
    config = {
        'listen_host': ('::0', 0, 1),
        'listen_port': 53,
        'path' : './root.json',
        'debug' : False,
    }

    server = DJServer(**config)
    server.bind()
    try:
        drop_priveleges(arguments['-u'], arguments['-g'])
    except:
        traceback.print_exc()
        server.stop()

    server.thread = serve_threaded(server)
    serve_wait(server)
