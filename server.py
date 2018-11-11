from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def format(message):
    """Formats the message into bytes"""

    return bytes(message, "utf-8")


def accept_incoming_connections():
    """Sets up handling for incoming clients."""

    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        clients[client] = 1
        client_handle_thread = Thread(target=handle_client, args=(client,))
        client_handle_thread.start()


def handle_client(client):
    """Handles a single client connection."""

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg)
        else:
            client.send(format("{quit}"))
            client.close()
            del clients[client]
            broadcast(format("Someone left the chat"))
            break


def broadcast(msg, prefix=""):
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}


if __name__ == "__main__":
    HOST = ''
    PORT = int(input("PORT : "))
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print("Echo server started on %s..." % PORT)
    accept_incoming_connections()
    server.close()
