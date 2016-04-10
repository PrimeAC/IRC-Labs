import socket

# Recebe no porto SERVER PORT os comandos "IAM <nome>", "HELLO",
#    "HELLOTO <nome>" ou "KILLSERVER" 
# "IAM <nome>" - regista um cliente como <nome>
# "HELLO" - responde HELLO ou HELLO <nome> se o cliente estiver registado
# "HELLOTO <nome>" - envia HELLO para o cliente <nome>
# "KILLSERVER" - mata o servidor

#INICIALIZACAO

SERVER_PORT=12001

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('',12001))

addrs   = {} # dict: nome -> endereco. Ex: addrs["user"]=('127.0.0.1',17234)
clients = {} # dict: endereco -> nome. Ex: clients[('127.0.0.1',17234)]="user"
status = {} # dict: nome -> estado. Ex: status["user"]=("occupied" or "available")


#FUNCOES DE CADA OPERACAO
def acknowledge():
    respond_msg = "OK" + "\n"
    server.sendto(respond_msg.encode().addr) 

def error(message):
  respond_msg = "NOK:" + message + "\n" 

def register_client(name,addr):
  # se o nome nao existe e o endereco nao esta a ser usado
  if not name in addrs and not addr in clients and not name in status:
    addrs[name] = addr
    clients[addr] = name
    status[name] = "available"

def remove_client(addr):
  if (addr in clients): #se addr estiver no dicinario clients, o utilizador existe
    temp_name=clients[addr]
    print(temp_name)
    del addr[temp_name]
    del status[temp_name]
    del clients[addr]

def return_list():
  respond_msg = "LSTR:"
  for key in status:
    respond_msg = respond_msg + (key + ":" + status[key] + ";")
  
  server.sendto(respond_msg.encode(),addr)

def respond_error(addr):
  respond_msg = "INVALID MESSAGE\n"
  server.sendto(respond_msg.encode(),addr)

#CORPO PRINCIPAL

while True:
  (msg,addr) = server.recvfrom(1024)
  cmds = msg.decode().split()
  if(cmds[0]=="REG"):
    register_client(cmds[1],addr)
  elif(cmds[0]=="EXIT"):
    remove_client(addr)
  elif(cmds[0]=="LST"):
    return_list()
  elif(cmds[0]=="KILLSERVER"):
    break
  else:
    respond_error(addr)

server.close()
