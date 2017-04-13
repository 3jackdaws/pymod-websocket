import redis
from settings import SSL_KEY, SSL_CERT
from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler
from tornado.web import Application

class IsoWebsocketHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, channel):
        self.redis = r.pubsub()
        self.redis.subscribe(**{channel:self.on_redis_message})
        self.channel = channel
        self.poll_thread = self.redis.run_in_thread(0.01)

    def on_message(self, message):
        r.publish(self.channel, message)

    def on_redis_message(self, message):
        if message['type'] == 'message':
            self.write_message(message['data'].decode('utf-8'))


    def on_close(self):
        self.poll_thread.stop()
        self.redis.close()


r = redis.StrictRedis(host='isogen.net', port='6379', password="BQ^Q^%CcsrRTsQN$^B^%MWJK<*(MLKS)")

if __name__ == "__main__":
    iso_app = Application([
        (r'/([a-zA-Z0-9_-]+)', IsoWebsocketHandler)
    ])
    server = HTTPServer(iso_app, ssl_options={
       "certfile": "/var/www/ssl/isogen.net/fullchain.pem",
       "keyfile": "/var/www/ssl/isogen.net/privkey.pem",
    })
    print("Running application")
    server.listen(8000)
    IOLoop.instance().start()