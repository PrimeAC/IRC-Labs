import socket

# Recebe no porto SERVER PORT os comandos "IAM <nome>", "HELLO",
#    "HELLOTO <nome>" ou "KILLSERVER" 
# "IAM <nome>" - regista um cliente como <nome>
# "HELLO" - responde HELLO ou HELLO <nome> se o cliente estiver registado
# "HELLOTO <nome>" - envia HELLO para o cliente <nome>
# "KILLSERVER" - mata o servidor

#INICIALIZACAO

SERVER_PORT=12000

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('',12000))

addrs   = {} # dict: nome -> endereco. Ex: addrs["user"]=('127.0.0.1',17234)
clients = {} # dict: endereco -> nome. Ex: clients[('127.0.0.1',17234)]="user"
status = {} # dict: nome -> estado. Ex: status["user"]=("occupied" or "available")


#FUNCOES DE CADA OPERACAO
def acknowledge(addr):
	respond_msg = "OK" + "\n"
	server.sendto(respond_msg.encode(),addr) 

def error(message,addr):
	respond_msg = "NOK:" + message + "\n" 
  	server.sendto(respond_msg.encode(),addr)

def register_client(name,addr):
	# se o nome nao existe e o endereco nao esta a ser usado
	if not name in addrs and not addr in clients and not name in status:
		addrs[name] = addr
		clients[addr] = name
		status[name] = "available"
		acknowledge(addr)

  	else:
  		error("Username already in use", addr)

def remove_client(addr):
	if (addr in clients): #se addr estiver no dicinario clients, o utilizador existe
		temp_name=clients[addr]
		del addrs[temp_name]
		del status[temp_name]
		del clients[addr]
		acknowledge(addr)

	else:
		error("User not registered", addr)

def return_list(addr):
	if addr in clients:
		respond_msg = "LSTR:"

		for key in status:
			print("key")
			print(key)
			print("status")
			print(status[key])
			respond_msg = respond_msg + key + ":" + status[key] + ";"

		server.sendto(respond_msg.encode(),addr)

	else:
		error("Access Denied!", addr)

def invite(addr, dest):
	if status[dest]=="available":
		daddr = addrs[dest]
		status[addr]="occupied"
		respond_msg="INV " + addr + " "+ dest
		print respond_msg
		server.sendto(respond_msg.encode(),daddr)

	else:
		if dest in addrs:
			error("User not available", addr)
		else:
			error("User does not exist", addr)

def invite_response(addr, dest, reply):
	if reply=="accept":

		if status[clients[addr]]=="occupied":
			respond_msg="INVR " + clients[addr] + " rejected"
			server.sendto(respond_msg.encode(), addrs[dest])

		else:
			status[clients[addr]]="occupied"
			respond_msg="INVR " + clients[addr] + " accept"
			server.sendto(respond_msg.encode(), addrs[dest])
	else:
		respond_msg="INVR " + clients[addr] + " rejected"
		server.sendto(respond_msg.encode(), addrs[dest])

def respond_error(addr):
	respond_msg = "INVALID MESSAGE\n"
	server.sendto(respond_msg.encode(),addr)

#CORPO PRINCIPAL

while True:
  (msg,addr) = server.recvfrom(1024)
  cmds = msg.split()
  if(cmds[0]=="REG"):
    register_client(cmds[1],addr)
  elif(cmds[0]=="EXIT"):
    remove_client(addr)
  elif(cmds[0]=="LST"):
    return_list(addr)
  elif(cmds[0]=="INV"):
    invite(cmds[1], cmds[2])
  elif(cmds[0]=="INVR"):
  	invite_response(addr, cmds[1], cmds[2])
  elif(cmds[0]=="KILLSERVER"):
    break
  else:
    respond_error(addr)

server.close()

