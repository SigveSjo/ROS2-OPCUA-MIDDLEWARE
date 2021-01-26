import socket
from threading import Thread

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 50008        # The port used by the server

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((HOST, PORT))

def receive():
    while True:
        data = soc.recv(1024)
        print('Received', repr(data))

def send():
    while True:
        msg = input("Enter message: ")
        soc.sendall(msg.encode("UTF-8"))


if __name__ == '__main__':
    Thread(target = receive).start()
    Thread(target = send).start()