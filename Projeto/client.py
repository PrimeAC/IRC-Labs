import socket
import sys
import select

SERVER_PORT = 12000
SERVER_IP   = '127.0.0.1'

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# o select quer ficar a espera de ler o socket e ler do stdin (consola)
inputs = [sock, sys.stdin]

#FUNCOES DE CADA OPERACAO
def acknowledge(dest):
  respond_msg = "OK " + dest + "\n"
  sock.sendto(respond_msg.encode(), (SERVER_IP, SERVER_PORT)) 

def replyInvitation(sender, to, reply):

  if reply == "Y\n":
    msg = "INVR " + sender + " " + to + " accept"
    sock.sendto(msg.encode(), (SERVER_IP,SERVER_PORT))

  else:
    msg = "INVR " + sender + " " + to + " reject"
    sock.sendto(msg.encode(), (SERVER_IP,SERVER_PORT))

def readList(msg):
  i=0
  aux=""
  print "Message received from server:"
  print "LSTR:"
  while i < len(msg):
    aux=aux+msg[i]
    if msg[i] == ";":
      print aux
      aux=""
    i+=1


#CORPO PRINCIPAL
while True:
  print("Input message to server below:")
  ins, outs, exs = select.select(inputs,[],[])
  #select devolve para a lista ins quem esta a espera de ler
  for i in ins:
    # i == sys.stdin - alguem escreveu na consola, vamos ler e enviar
    if i == sys.stdin:
      # sys.stdin.readline() le da consola
      msg = sys.stdin.readline()
      # envia mensagem da consola para o servidor
      sock.sendto(msg.encode(),(SERVER_IP,SERVER_PORT))
    # i == sock - o servidor enviou uma mensagem para o socket
    elif i == sock:
      (msg,addr) = sock.recvfrom(1024)
      cmds = msg.split()

      if cmds[0] == "LSTR:":
        acknowledge("server")
        readList(cmds[1])
        break

      if cmds[0] == "INV":
        acknowledge(cmds[1])
        print("Received invite from " + cmds[1])
        print("Type [Y] to accept or [N] to deny:")
        msg = sys.stdin.readline()
        replyInvitation(cmds[2],cmds[1], msg)
        break

      if cmds[0] == "INVR":
        print("Player " + cmds[1] + " has " + cmds[2] + " your inivitation")
        acknowledge(cmds[1])
        break
      
      print "Message received from server:", cmds[0]