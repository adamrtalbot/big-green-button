#!/usr/bin/env python3
"""
Gunicorn configuration file for the Studios Launch Page application.
"""

import os
import multiprocessing

# Server socket
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:5000")
backlog = 2048

# Worker processes
workers = os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1)
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = None


# Server hooks
def on_starting(server):
    print("Starting Gunicorn server for Studios Launch Page")


def on_exit(server):
    print("Shutting down Gunicorn server for Studios Launch Page")
