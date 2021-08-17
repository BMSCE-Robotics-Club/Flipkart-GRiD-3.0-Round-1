import socket

# Create a client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Connect to the server
clientSocket.connect(("localhost",9999))


# Send data to server
data = "Hey Server!"
clientSocket.send(data.encode())


# Receive data from server
dataFromServer = clientSocket.recv(1024)

 
# Print to the console
print(dataFromServer.decode())

 