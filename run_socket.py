import pymod_ws

from pymod_ws.wss import load_modules, IsoGetHandler, IsoWebsocketHandler
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


if __name__ == "__main__":
    load_modules()
    iso_app = Application([
        (r'/ws/?(.*?)/(.*)', IsoWebsocketHandler),
        (r'/api/?(.*?)/(.*)', IsoGetHandler)
    ])
    server = HTTPServer(iso_app, ssl_options={
        "certfile": "/var/www/ssl/isogen.net/fullchain.pem",
        "keyfile": "/var/www/ssl/isogen.net/privkey.pem",
    })
    server.listen(8000)
    IOLoop.instance().start()