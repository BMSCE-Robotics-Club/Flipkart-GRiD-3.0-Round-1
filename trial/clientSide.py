import socket
import threading
import time


HOST = '192.168.0.111'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


def my_client():
    threading.Timer(11, my_client).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        data = s.recv(1024).decode('utf-8')

        print(data)

        s.close()
        # time.sleep(5)


if __name__ == "__main__":
    while 1:
        my_client()
