#!/usr/bin/env python
'''
usage: scrape.py [ -o OUTPUT ]

HypeDNS scraper. Pulls data from HypeDNS, and transforms it into a DJDNS doc.
Should generally be run to output to tlds/hype/generated.json.

options:
    -h --help   Show this message.
    -o OUTPUT   Output file to save to, '-' for STDOUT [default: ./tlds/hype/generated.json]
'''

from __future__ import print_function

from docopt import docopt
import json
import re
import requests
import socket
import sys

METADATA = {
    'about' : 'Data automatically harvested from HypeDNS with scraper.py',
}

def make_selector(hostname):
    return '^' + re.escape(hostname.lower()) + '$'

def make_branch(host):
    hostname = host['name']
    ip = host['ip']

    # Filter out entries with invalid IP addrs
    try:
        socket.inet_pton(socket.AF_INET6, ip)
    except:
        return

    if not "." in hostname:
        hostname += '.hype'

    return {
        'selector' : make_selector(hostname),
        'records'  : [
            {
                'domain_name': hostname,
                'rtype': 'AAAA',
                'rdata': ip
            }
        ],
        'targets'  : [],
    }

def get_data():
    r = requests.get('http://[fc5d:baa5:61fc:6ffd:9554:67f0:e290:7535]/nodes/list.json')
    return r.json()['nodes']

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1')
    path = arguments['-o']
    if path == '-':
        output = sys.stdout
    else:
        output = open(path, 'w')

    data = get_data()
    data.sort(key = lambda x: x['name'])
    contents = {
        'meta' : METADATA,
        'branches': [   branch for branch in 
                        (make_branch(host) for host in data)
                        if branch != None
                    ]
    }
    json.dump(contents, output, indent=4)
