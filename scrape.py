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
import sys

METADATA = {
    'about' : 'Data automatically harvested from HypeDNS with scraper.py',
}

def make_selector(hostname):
    return '^' + re.escape(hostname + '.hype') + '$'

def make_branch(host):
    hostname = re.sub('\\.hype$', '', host['name'])
    ip = host['ip']

    return {
        'selector' : make_selector(hostname),
        'records'  : [
            {
                'domain_name': hostname + '.hype',
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
        'branches': [make_branch(host) for host in data]
    }
    json.dump(contents, output, indent=4)
