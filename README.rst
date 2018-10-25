Health check for PostgreSQL + repmgr
====================================

This package is intended to be used as an health check backend for HAProxy. It
provides a small script that will run an HTTP server querying each PostgreSQL
servers of the replication cluster to know the role (primary, standby, witness
or fenced) of the local instance according to the majority of them (kind of a
vote).

Usage and configuration example to come…

TODO: make use of Tornado for HTTP server
TODO: make use of asyncio for SQL queries
TODO: split HTTP server and SQL queries in two modules to allow running SQL part through a CLI program
TODO: replace json by toml (with backward compatibility)
TODO: use poetry for dependencies management and packaging
TODO: handle environment variables for config (with os.environ.get(x))

