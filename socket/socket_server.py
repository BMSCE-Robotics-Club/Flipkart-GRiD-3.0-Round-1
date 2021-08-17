import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

 

# Bind and listen

serverSocket.bind(("localhost",9999))

serverSocket.listen()
print("waiting for connections:")
 

# Accept connections

while(True):

    (clientConnected, clientAddress) = serverSocket.accept()
    print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]))   

    dataFromClient = clientConnected.recv(1024)
    print(dataFromClient.decode())

    # Send some data back to the client
    clientConnected.send("Hey Client!".encode())