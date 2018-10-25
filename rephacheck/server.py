#!/usr/bin/env python

"""
Run RepHACheck HTTP server.
"""

import tornado.ioloop  # type: ignore
from tornado.options import define, options, parse_command_line  # type: ignore
import tornado.web  # type: ignore

from rephacheck.config import config
from rephacheck.query import node_state_quorum

define("address", default="127.0.0.1", help="listen on the given address", type=str)
define("port", default=8543, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode", type=bool)


class MainHandler(tornado.web.RequestHandler):
    """Main requests handler."""

    def data_received(self, chunk):
        """Do nothing of recevied data."""
        pass

    def get(self, *args, **kwargs):
        """Output node state on GET."""
        state = node_state_quorum(config())
        self.write(state)


def main():
    """Run HTTP server."""

    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
        ],
        debug=options.debug,
    )
    app.listen(options.port, options.address)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
