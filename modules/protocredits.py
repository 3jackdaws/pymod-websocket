

endpoint = "protocredits"

def on_request(request, message):
    print(request, message)

def on_message(websocket, arguments, message):
    print(message)

def on_open(websocket, path):
    print(path)

