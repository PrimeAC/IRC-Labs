import socket

ClientMsg = 'Hello World!'
print("Client running")
ClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ClientSock.sendto(ClientMsg, ('127.0.0.1', 5005))
print("Message to server: ", ClientMsg)
(ServerMsg, (ClientIP, ClientPort)) = ClientSock.recvfrom(100)
print("Message from server: ", ServerMsg)
ClientSock.close()