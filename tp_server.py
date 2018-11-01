import socket
import random
import threading
from Queue import Queue

##############################################################################################################################
#This code has been taken from the optional lecture and has been modified to suit my needs, but the archetecture is not mine.
##############################################################################################################################

HOST = ""
PORT = 50003
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)

def handleClient(client, serverChannel, cID, clientele): 
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8") 
      command = msg.split("\n") 
      while (len(command) > 1): 
        readyMsg = command[0]
        msg = "\n".join(command[1:]) 
        serverChannel.put(str(cID) + "_" + readyMsg) 
        command = msg.split("\n") 
    except: 
      clientele.pop(cID)
      return

def serverThread(clientele, serverChannel): 
  readyClient = 0
  while True:
    msg = serverChannel.get(True, None) 
    senderID, msg = int(msg.split("_")[0]), "_".join(msg.split("_")[1:])
    if (msg): 
      if "ready" in msg:
        readyClient += 1
        if readyClient == 1:
          for cID in clientele: 
            if cID != senderID: 
              sendMsg = msg + "\n" 
              clientele[cID].send(sendMsg.encode())
      if "finish" in msg:
        for i in range(15):
          if i in clientele:
            del clientele[i]
      if "ready" not in msg:
        for cID in clientele: 
          if cID != senderID: 
            sendMsg = msg + "\n" 
            clientele[cID].send(sendMsg.encode()) 
      if "quit" in msg:
        for i in range(15):
          if i in clientele:
            del clientele[i]
    if readyClient >= 2:
      for cID in clientele:
        if cID % 2 == 0:
          clientele[cID].send(("allPlayer true\n").encode())
        else:
          clientele[cID].send(("allPlayer false\n").encode())
      readyClient = 0
    serverChannel.task_done() 

clientele = {}
currID = 0

serverChannel = Queue(100) #initialize Q
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start() #setting up threading (dont change)


while True: #loop for adding clients
  client, address = server.accept()
  if len(clientele) < 2: # so that at one time there are only 2 clients on the server
    for cID in clientele: #loop through all other client IDs to tell them we are adding a new player
      clientele[cID].send(("newPlayer %d 100 100\n" % currID).encode()) #sending string with new player info to other clients
      client.send(("newPlayer %d 100 100\n" % cID).encode()) #send info to new client about old player
    clientele[currID] = client #assigning a dictionary spot for new client
    if len(clientele) == 2:
      for cID in clientele:
        clientele[cID].send(("bothPlayer\n").encode())
    threading.Thread(target = handleClient, args = 
                          (client ,serverChannel, currID, clientele)).start()
  #start thread for handling that clients messages
    currID += 1
  else:
    client.send(("Too late\n").encode())
