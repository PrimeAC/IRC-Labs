import socket

ClientMsg = 'Hello World!'
print("Client running")
ClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ClientSock.sendto(ClientMsg.encode(), ('192.168.56.101', 5005))
print("Message to server: ", ClientMsg)
(ServerMsg, (ClientIP, ClientPort)) = ClientSock.recvfrom(100)
print("Message from server: ", ServerMsg.decode())
ClientSock.close()