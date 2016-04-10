import socket

ServerMsg = 'Nice to meet you !'
print("Server running")
ServerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ServerSock.bind (('', 5005))
(ClientMsg, (ClientIP, ClientPort)) = ServerSock.recvfrom(100)
ServerSock.sendto(ServerMsg, (ClientIP, ClientPort))
ServerSock.close()