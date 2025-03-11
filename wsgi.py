#!/usr/bin/env python3
"""
WSGI entry point for the Studios Launch Page application.
This file is used when deploying the application with a WSGI server.
"""

from app import application

if __name__ == "__main__":
    application.run()
