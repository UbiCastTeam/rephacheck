#!/usr/bin/env python3

"""
Determine by voting which is the state of each node.
For this to work properly, you need to have an odd number of nodes.
"""

# TODO: import asyncio
from collections import Counter

import psycopg2  # type: ignore

from rephacheck.config import config


def node_state(node_id: int, conninfo: dict) -> tuple:
    """Get the given node state.

    :param node_id: Node ID for which we want the state
    :type node_id: int
    :param conninfo: PostregSQL connection string
    :type conninfo: dict
    :param timeout: Timeout value
    :type timeout: int
    :return: Return a tuple with "active" and "type" state of the wanted node
    :rtype: tuple
    """

    try:
        # postgresql query
        con = psycopg2.connect(**conninfo)
        cur = con.cursor()
        query = "SELECT active, type FROM repmgr.nodes WHERE node_id = {};"
        cur.execute(query.format(node_id))
        state = cur.fetchone()
        cur.close()
    except psycopg2.Error:
        # an error occured, return false by default
        state = (False, "unknown")

    return state


def node_state_quorum(conf: dict) -> str:
    """Get a quorum about node state.

    :param conf: Configuration options
    :type conf: dict
    :return: Quorum about node state
    :rtype: str
    """

    # init vars
    votes = []
    quorum_state = "unknown"

    # ask each node for the state of the local node
    for node in conf["nodes"].values():
        conninfo = conf["conninfo"].update({"host": node["addr"], "port": node["port"]})
        active, role = node_state(node["local_node_id"], conninfo)
        # if node considered active take vote, otherwise fence it
        if active:
            votes.append(role)
        else:
            votes.append("fenced")

    # determines result by voting
    results = Counter(votes)
    if results:
        quorum_state = results.most_common(1)[0][0]

    return quorum_state


def main():
    """Print node state.

    :return: Node state
    :rtype: str
    """

    state = node_state_quorum(config())
    print(state)


if __name__ == "__main__":
    main()
