import pymod_ws

from pymod_ws.wss import load_modules, IsoGetHandler, IsoWebsocketHandler
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from settings import SSL_CERT, SSL_KEY


if __name__ == "__main__":
    load_modules()
    iso_app = Application([
        (r'/ws/?(.*?)/(.*)', IsoWebsocketHandler),
        (r'/api/?(.*?)/(.*)', IsoGetHandler)
    ])
    server = HTTPServer(iso_app, ssl_options={
        "certfile": SSL_CERT,
        "keyfile": SSL_KEY,
    })
    server.listen(8000)
    IOLoop.instance().start()