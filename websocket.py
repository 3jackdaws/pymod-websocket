import asyncio
import websockets
import glob
import re
import os
import sys
import json

def load_modules():
    global modules
    module_names = glob.glob("modules/*.py")
    sys.path.append("modules")

    for module_name in module_names:
        import_name = re.findall("(modules\\\|/)([a-zA-Z0-9]+)",module_name)[0][1]
        mod = __import__(import_name)

        if not hasattr(mod, "endpoint"):
            print("Error when loading '{}' module: Message handler module must define an 'endpoint' property.".format(import_name))
            continue

        if not hasattr(mod, "on_message"):
            print("Error when loading '{}' module: Message handler module must possess a 'on_message' function.".format(import_name))
            continue

        if not asyncio.iscoroutinefunction(mod.on_message):
            print("Error when loading '{}' module: Message handler function 'on_message' must be a coroutine.".format(import_name))
            continue

        modules[mod.endpoint] = mod

    print("Loaded modules:\n{}".format("\n".join([x for x in modules])))


async def entrypoint(websocket:websockets.WebSocketClientProtocol, path):

    handler = None
    try:
        handler = modules[path[1:]]
        print("Install '{}' message handler for client with address '{}'.".format(path[1:], websocket.remote_address[0]))
    except:
        await websocket.send(json.dumps({
            "error":"The endpoint '{}' is not defined.".format(path)
        }))
        print("Client accessed invalid endpoint")
        websocket.close()
        return

    while 1:
        message = await websocket.recv()
        await handler.on_message(websocket, message)



modules = {}
load_modules()
start_server = websockets.serve(entrypoint, 'localhost', 8002)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()