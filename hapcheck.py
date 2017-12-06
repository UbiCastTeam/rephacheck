#!/usr/bin/env python

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import http.server
import psycopg2

PORT = 8000
NODES = {
    'pg1': {
        'addr': '10.64.249.79',
        'node_id': 1,
    },
    'pg2': {
        'addr': '10.64.249.188',
        'node_id': 2,
    },
    'pg3': {
        'addr': '10.64.249.155',
        'node_id': 3,
    },
}
CONN = {
    'dbname': 'repmgr',
    'user': 'repmgr',
    'password': 'changeme',
}


class Server(http.server.HTTPServer):
    pass


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.s = get_quorum_state(**NODES['pg1'])
        http.server.SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self.s)
        self.wfile.write('\n')

    def do_HEAD(self):
        self._set_headers()


def get_state(addr, node_id):
    try:
        # postgresql query
        con = psycopg2.connect(host=addr, **CONN)
        cur = con.cursor()
        query = 'SELECT active, type FROM repmgr.nodes WHERE node_id = {};'
        cur.execute(query.format(node_id))
        data = cur.fetchone()
        cur.close()
        # determine if is an active primary
        is_primary = True if data == (True, 'primary') else False
        # return result
        return is_primary
    except Exception:
        # an error occured, so return false by default
        return False


def get_quorum_state(addr, node_id):
    # init vars
    vote = 0
    state = 'standby'
    # ask each node for its state
    for node in NODES.values():
        vote += 1 if get_state(node['addr'], node_id) else 0
    # determines voting result
    if vote > len(NODES) / 2:
        state = 'primary'
    # return result
    return state


def run():
    # run http server
    httpd = Server(('localhost', PORT), Handler)
    print('serving at port', PORT)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
