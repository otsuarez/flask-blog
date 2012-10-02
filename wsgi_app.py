#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from blog import app, db


if __name__ == '__main__':
    WSGIServer(app).run()
    #WSGIServer(app, bindAddress='/tmp/myflask-fcgi.sock').run()


