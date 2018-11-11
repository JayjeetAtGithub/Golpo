from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import tkinter


def format(message):
    """Formats the message into bytes"""

    return bytes(message, "utf-8")


def recieve():
    """Recieve a message from server"""

    while True:
        try:
            msg = client_socket.recv(1024).decode("utf-8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break


def send(event=None):
    """Sends a message to the server"""

    msg = message.get()
    message.set("")
    client_socket.send(format(msg))
    if msg == "{quit}":
        client_socket.close()
        window.quit()


def on_closing(event=None):
    """Closes the connection"""

    message.set("{quit}")
    send()


# ---- GUI ----
window = tkinter.Tk()
window.title("Golpo")

msg_frame = tkinter.Frame(window)
message = tkinter.StringVar()
message.set("Type your message here.")
scrollbar = tkinter.Scrollbar(msg_frame)
msg_list = tkinter.Listbox(
    msg_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
msg_frame.pack()

entry_field = tkinter.Entry(window, textvariable=message)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(window, text="Send", command=send)
send_button.pack()


window.protocol("WM_DELETE_WINDOW", on_closing)
# ---- GUI ----

if __name__ == "__main__":
    HOST = ''
    PORT = int(input('PORT : '))
    ADDRESS = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDRESS)
    recieve_thread = Thread(target=recieve)
    recieve_thread.start()
    tkinter.mainloop()
