from tornado.websocket import WebSocketHandler
from tornado.web import Application, RequestHandler, asynchronous

import json
import glob
from os.path import basename, splitext
import sys
sys.path.append("modules")
from importlib import reload
import settings

loaded_modules = {}

def load_modules():
    global loaded_modules

    for module in settings.INSTALLED_MODULES:
        try:
            imported_module = __import__(module)
            module_compatible, failure_reason = check_requirements(imported_module)
            if module_compatible:
                loaded_modules[imported_module.endpoint] = imported_module
                print("Loaded module: [ {} ]".format(imported_module.__name__))
            else:
                print("Failed to load '{}':".format(imported_module.__name__), failure_reason)
        except Exception as e:
            print(e)

def check_requirements(module):
    if not hasattr(module, "endpoint"):
        return False, "module has not defined an 'endpoint' attribute."

    if not hasattr(module, "on_request"):
        return False, "module has no 'on_request' GET event handler."

    if not hasattr(module, "on_open"):
        return False, "module has no 'on_open' websocket event handler."

    if not hasattr(module, "on_message"):
        return False, "module has no 'on_message' websocket event handler."

    return True, "Module has all requirements."

class IsoWebsocketHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, endpoint, arguments):
        if endpoint in loaded_modules:
            self.endpoint = endpoint
            self.id = self.__hash__();
            print(self.id)
            self.handler = loaded_modules[endpoint]
            self.handler.on_open(self)
        else:
            self.send_error(status_code=404)
            self.close(1001, "Endpoint not available.")

    def on_message(self, message):
        self.handler.on_message(self, message)

    def on_close(self):
        self.handler.on_close(self)


class IsoGetHandler(RequestHandler):
    @asynchronous
    def get(self, endpoint, arguments):
        arguments = arguments.rsplit("/")
        return_dict = {}
        if endpoint in loaded_modules:
            return_dict = loaded_modules[endpoint].on_request(self, arguments)
        return_dict['api_version'] = "1.0"
        self.write(json.dumps(return_dict, indent=2))
        self.set_header("Content-Type", "application/json")
        self.finish()


