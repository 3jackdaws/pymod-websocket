
def send_to_all(clients, message):
    remove = []
    for socket in clients:

            socket.write_message(message)

    for sock in remove:
        clients.remove(sock)

def send_to_all_except(clients, except_client, message):
    for socket in clients:
        try:
            if socket != except_client:
                socket.write_message(message)
        except:
            pass