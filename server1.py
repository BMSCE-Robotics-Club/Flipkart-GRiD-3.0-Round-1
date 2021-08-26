import socket
import time 

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print('My IP: '+IPAddr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IPAddr, 80))
s.listen(0)                 

i = 0
x = 'f1'
while True:
    client, addr = s.accept()
   # client.settimeout(3)
    
    while True:
        """content = client.recv(1024)
        if len(content) == 0:
           break
        if str(content,'utf-8') == '\r\n':
            continue
        if i%2 == 0:
            if x == 's1':
                x = 'f1'
            else:
                x = 's1'"""
        
        print(x)
        client.send(bytes(x, 'utf-8'))
        i = i+1
    #client.close()
        
