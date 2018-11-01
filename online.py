from Tkinter import *
import string
import tkMessageBox
import tkSimpleDialog
import pickle
import os
import random
import socket
import threading
from Queue import Queue
import main

##############################################################################################################################
# This function has been taken from optional lecture for sockets.
##############################################################################################################################

def handleServerMsg(server, serverMsg):
  server.setblocking(1) #takes messages from server and puts them on Q
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg) #adds message on the queue
      command = msg.split("\n")


def multiInit(data):
    HOST = ""
    PORT = 50003
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.connect((HOST,PORT))
    serverMsg = Queue(100)
    threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
    # The above code is for sockets which was taken from the optional lecture and is not mine
    data.server = server
    data.serverMsg = serverMsg
    data.rows = 10
    data.cols = 10
    data.player1Turn = True
    data.player2Turn = False
    data.player1Ships = []
    data.player2Ships = []
    data.chooseMode = True
    data.playMode = False
    data.selector = [0,0]
    data.availShips = [5,4,3,3,2]
    data.shipIndex = 0
    data.shipDictionary1 = dict()
    data.shipDictionary2 = dict()
    for i in range(5):
        data.shipDictionary1[i] = []
    data.shipName = dict()
    data.shipName[0] = "Carrier"
    data.shipName[1] = "Battleship"
    data.shipName[2] = "Cruiser"
    data.shipName[3] = "Subspacer"
    data.shipName[4] = "Destroyer"
    data.selected = False
    data.vertical = True
    data.player1Guess = []
    data.player2Guess = []
    data.placed = 0
    data.placedList = []
    data.hit = False
    data.miss = False
    data.timer = 1000
    data.player2ShipList = [0,1,2,3,4]
    data.player1ShipList = [0,1,2,3,4]
    data.bothPlayers = False
    data.gameOver = False
    data.depletedShips = False
    data.imageDictionary1 = {}
    data.imageDictionary2 = {}
    data.dupSelector1 = []
    data.dupSelector2 = []
    data.animRad = 15


def doMouseChoose(event,data):
    if (60 <= event.x <= 260) and (70 <= event.y <= 90):
        if 0 not in data.placedList:
            data.selected = True
            data.shipIndex = 0
    elif (60 <= event.x <= 220) and (120 <= event.y <= 140):
        if 1 not in data.placedList:
            data.selected = True
            data.shipIndex = 1
    elif (60 <= event.x <= 180) and (170 <= event.y <= 190):
        if 2 not in data.placedList:
            data.selected = True
            data.shipIndex = 2
    elif (60 <= event.x <= 180) and (220 <= event.y <= 240):
        if 3 not in data.placedList:
            data.selected = True
            data.shipIndex = 3
    elif (60 <= event.x <= 140) and (270 <= event.y <= 290):
        if 4 not in data.placedList:
            data.selected = True
            data.shipIndex = 4
    elif (150 <= event.x <= 235) and (425 <= event.y <= 450):
        if data.player1Turn:
            data.player1Ships = []
            for i in range(5):
                data.shipDictionary1[i] = []
        else:
            data.player2Ships = []
            for i in range(5):
                data.shipDictionary2[i] = []
        data.placedList = []
        data.selected = False
        data.selector = [0,0]
        data.placed = 0
        data.imageDictionary1 = {}
    elif (600 <= event.x <= 685) and (75 <= event.y <= 100):
        if tkMessageBox.askokcancel("Are you sure?", "You will be sent to the main screen!"):
            msg = "quit\n"
            data.server.send(msg.encode())
            main.init(data.canvas,data)
    elif (600 <= event.x <= 685) and (25 <= event.y <= 50):
        if data.placed == 5:
            if tkMessageBox.askokcancel("Are you sure?", "You will not be able to change the location of your ships"):
                data.chooseMode = False 
                msg = "ready\n"
                data.server.send(msg.encode())
        else:
            title = "Error"
            message = "You have not hid all the ships!"
            tkMessageBox.showinfo(title,message)
    elif  data.selected and (300 <= event.x <= 700) and (100 <= event.y <= 500):
        row,col = getCell(data,event.x,event.y,300,100,40)
        data.selector[0] = row
        data.selector[1] = col
        if data.vertical:
            if data.selector[0] +  data.availShips[data.shipIndex] > 9:
                data.selector[0] = 10 - data.availShips[data.shipIndex]
        else:
            if data.selector[1] +  data.availShips[data.shipIndex] > 9:
                data.selector[1] = 10 - data.availShips[data.shipIndex]
    else:
        data.selected = False

def getCell(data,x,y,startX,startY,size):
    row = (y - startY) / size
    col = (x - startX) / size
    return (row,col)

def doMousePlay(event,data):
    if (600 <= event.x <= 685) and (25 <= event.y <= 500):
        if tkMessageBox.askokcancel("Are you sure?", "You will be sent to the main screen!"):
            msg = "quit\n"
            data.server.send(msg.encode())
            main.init(data.canvas,data)
    elif  data.select and (10 <= event.x <= 310) and (200 <= event.y <= 500):
        row,col = getCell(data,event.x,event.y,10,200,30)
        data.selector[0] = row
        data.selector[1] = col

def doOnMultiMouse(event,data):
    if data.chooseMode and data.bothPlayers:
        doMouseChoose(event,data)
    elif data.playMode:
        doMousePlay(event,data)

def mousePressed(event, data):
    if data.onMulti:
        doOnMultiMouse(event,data)


def doOnMultiChooseReturn(event,data):
    if event.keysym == "Return":
        L = []
        addToList = True
        for i in range(data.availShips[data.shipIndex]):
            if data.vertical:
                tup = (data.selector[0]+i,data.selector[1])
                if tup in data.player1Ships:
                    title = "Error"
                    message = "Ship Already There"
                    tkMessageBox.showinfo(title, message)
                    addToList = False
                    break
            else:
                tup = (data.selector[0],data.selector[1]+i)
                if tup in data.player1Ships:
                    title = "Error"
                    message = "Ship Already There"
                    tkMessageBox.showinfo(title, message)
                    addToList = False
                    break
            L.append(tup)
        if addToList:
            data.player1Ships.extend(L)
            #the following if else statments are to make the dictionary which will be used to draw the images correctly
            if data.vertical:
                data.imageDictionary1[data.shipImages[data.shipIndex][1]] = [data.selector[0],data.selector[1],1,data.availShips[data.shipIndex],data.shipIndex]
                data.imageDictionary2[data.smallShipImages[data.shipIndex][1]] = [data.selector[0],data.selector[1],1,data.availShips[data.shipIndex],data.shipIndex]
            else:
                data.imageDictionary1[data.shipImages[data.shipIndex][0]] = [data.selector[0],data.selector[1],0,data.availShips[data.shipIndex],data.shipIndex]
                data.imageDictionary2[data.smallShipImages[data.shipIndex][0]] = [data.selector[0],data.selector[1],0,data.availShips[data.shipIndex],data.shipIndex]
            data.selector[0],data.selector[1] = 0,0
            data.placedList.append(data.shipIndex)
            data.shipDictionary1[data.shipIndex].extend(L)
            data.selected = False
            data.placed += 1
                

def doKeyChooseMode(event,data):
    if data.selected:
        if event.keysym == "Up":
            if 0 < data.selector[0]: data.selector[0] -= 1
        elif event.keysym == "Down":
            if data.vertical:
                if 10 > data.selector[0] + data.availShips[data.shipIndex]: data.selector[0] += 1
            else:
                if 9 > data.selector[0]: data.selector[0] += 1
        elif event.keysym == "Right":
            if data.vertical:
                if 9 > data.selector[1]: data.selector[1] += 1
            else:
                if 10 > data.selector[1] + data.availShips[data.shipIndex]: data.selector[1] += 1
        elif event.keysym == "Left":
                if 0 < data.selector[1]: data.selector[1] -= 1
        elif event.keysym == "space":
            if data.vertical:
                if data.selector[1] +  data.availShips[data.shipIndex] > 9:
                    data.selector[1] = 10 - data.availShips[data.shipIndex]
            else:
                if data.selector[0] +  data.availShips[data.shipIndex] > 9:
                    data.selector[0] = 10 - data.availShips[data.shipIndex]
            data.vertical = not data.vertical
        if data.selected == True:
            if data.onMulti:
                doOnMultiChooseReturn(event,data)


def doOnKeyPlayReturn(event,data):
    if event.keysym == "Return":
        canvas = data.canvas
        if data.player1Turn:
            if (data.selector[0],data.selector[1]) in data.player1Guess:
                title = "Error"
                message = "You've Already Attacked There"
                tkMessageBox.showinfo(title, message)
                return
            data.dupSelector1 = data.selector
            data.select = False 
            data.player1Guess.append((data.selector[0],data.selector[1]))
            msg = "attack%d%d\n" %(data.selector[0],data.selector[1])
            data.server.send(msg.encode())


def doKeyPlayMode(event,data):
    if data.select:
        if event.keysym == "Up":
            if 0 < data.selector[0]: data.selector[0] -= 1
        elif event.keysym == "Down":
            if 9 > data.selector[0]: data.selector[0] += 1
        elif event.keysym == "Right":
            if 9 > data.selector[1] : data.selector[1] += 1
        elif event.keysym == "Left":
            if 0 < data.selector[1]: data.selector[1] -= 1
        if data.onMulti:
            doOnKeyPlayReturn(event,data)
    

def doKeyOnMulti(event,data):
    if data.chooseMode and data.bothPlayers:
        doKeyChooseMode(event,data)
    elif data.playMode:
        if data.player1Turn:
            doKeyPlayMode(event,data)

def keyPressed(event, data):
    if data.onMulti:
        doKeyOnMulti(event,data)

def doHit(data,tup):
    for i in range(5):
        if i in data.player1ShipList:
            if tup in data.shipDictionary1[i]:
                data.shipDictionary1[i].remove(tup)
                break
    for i in range(5):
        if i in data.player1ShipList and len(data.player1ShipList) > 1:
            if len(data.shipDictionary1[i]) == 0:
                del data.shipDictionary1[i]
                name = data.shipName[i]
                msg = "destroyedShip%d\n" %(i)
                data.server.send(msg.encode())
                title = "Oh No!"
                message = "Your %s has been destroyed" %(name)
                tkMessageBox.showinfo(title,message)
                data.player1ShipList.remove(i)
                return 
    if len(data.player1ShipList) == 1:
        for i in range(5):
            if i in data.player1ShipList:
                if len(data.shipDictionary1[i]) == 0:
                    msg = "gameOver\n" 
                    data.server.send(msg.encode())
                    data.depletedShips = True
                    return 
    msg = "hit\n"
    data.server.send(msg.encode())
    data.miss = False
    data.hit = True


def doMiss(data):
    msg = "miss\n"
    data.server.send(msg.encode())
    data.player1Turn = True
    data.selector = [0,0]
    data.hit = False
    data.miss = True
    data.select = True





def doOnMultiTimerFired(data):
    if data.depletedShips:
        title = "Loss!"
        message = "Your opponent won the Game!"
        tkMessageBox.showinfo(title, message)
        main.init(data.canvas,data)

    if data.miss or data.hit:
        if data.timer > 0:  
            data.timer -= data.timerDelay
            data.animRad -= 1.5
        else:
            data.miss = False
            data.hit = False
            data.timer = 1000
            data.animRad = 15
            data.select = True
    # the following is the code which deals with all kinds of messages that are recieved from the other player via the server
    # depending on the message, the program reacts accordingly
    if (data.serverMsg.qsize() > 0):
        msg = data.serverMsg.get(False) 
        try:
            if msg.startswith("bothPlayer"): 
                data.bothPlayers = True
            elif msg.startswith("allPlayer true"):
                data.playMode = True
                data.player1Turn = True
                data.select = True 
            elif msg.startswith("allPlayer false"):
                data.playMode = True
                data.player1Turn = False
                data.select = False
            elif "attack" in msg:
                tup = (int(msg[-2]),int(msg[-1]))
                data.dupSelector2 = [tup[0],tup[1]]
                data.player2Guess.append(tup)
                if tup in data.player1Ships:
                    doHit(data,tup)
                else:
                    doMiss(data)
            elif msg.startswith("hit"):
                data.player2Ships.append((data.selector[0],data.selector[1]))
                data.miss = False
                data.hit = True 
            elif msg.startswith("miss"):
                data.player1Turn = False
                data.hit = False
                data.miss = True
            elif msg.startswith("gameOver"):
                data.player2Ships.append((data.selector[0],data.selector[1]))
                data.miss = False
                data.hit = True
                data.gameOver = True
                if data.gameOver:
                    title = "Congaratulations!"
                    message = "You Win!"
                    tkMessageBox.showinfo(title, message)
                    msg = "finish\n"
                    data.server.send(msg.encode())
                    main.init(data.canvas,data)
            elif msg.startswith("destroyedShip"):
                data.player2Ships.append((data.selector[0],data.selector[1]))
                data.miss = False
                data.hit = True
                name = data.shipName[int(msg[-1])]
                title = "Congratulations!"
                message = "You have destroyed the enemy's %s" %(name)
                tkMessageBox.showinfo(title,message)
            elif msg.startswith("quit"):
                title = "Game Over!"
                message = "The other player has quit the game"
                tkMessageBox.showinfo(title,message)
                main.init(data.canvas,data)
            elif msg.startswith("ready"):
                title = "Done!"
                message = "The other player is done hiding ships!"
                tkMessageBox.showinfo(title,message)

        except:
            print("failed")
        data.serverMsg.task_done()

def timerFired(data):
    if data.onMulti:
        doOnMultiTimerFired(data)

def getBounds(row,col,startX,startY,size):
    x0 = startX + col*size
    x1 = startX + (col+1)*size
    y0 = startY + row*size
    y1 = startY + (row+1)*size
    return x0,y0,x1,y1

def drawGrid(canvas,startX,startY,size,data):
    rows,cols = data.rows,data.cols
    for row in range(rows):
        for col in range(cols):
            x0,y0,x1,y1 = getBounds(row,col,startX,startY,size)
            color = "white"
            if data.onMulti:
                if data.playMode:
                    if startX == 10:
                        if (row,col) in data.player1Guess and (row,col) in data.player2Ships: color = "green"
                        elif (row,col) in data.player1Guess : color = "red"
                        else: color = "ivory"
                    else:
                        if (row,col) in data.player2Guess and (row,col) in data.player1Ships: color = "green"
                        elif (row,col) in data.player2Guess : color = "red"
                        else: color = "lightCyan"
            if (row,col) in data.player1Ships and (startX != 10) and (data.playMode):
                canvas.create_rectangle(x0,y0,x1,y1,fill=color)
            else:
                canvas.create_rectangle(x0,y0,x1,y1,fill=color)

def drawSelectorChoose(canvas,data):
    selector = data.selector
    ind = data.shipIndex
    avail = data.availShips
    for i in range(avail[ind]):
        if data.vertical:
            x0,y0,x1,y1 = getBounds(selector[0]+i,selector[1],data.startX,data.startY,data.size)
        else:
            x0,y0,x1,y1 = getBounds(selector[0],selector[1]+i,data.startX,data.startY,data.size)
        canvas.create_rectangle(x0,y0,x1,y1,fill="yellow")

def getCellCoords(data,startX,startY,row,col,size,vertical,shipSize):
    margin = 0
    if shipSize == 5 or shipSize == 3:
        margin = 25
    if vertical == 1:
        x0 = startX + (col+0.5)*size
        y0 = startY + (row+shipSize/2)*size + margin
    else:
        x0 = startX + (col+shipSize/2)*size + margin
        y0 = startY + (row+0.5)*size
    return(x0,y0)


def drawChoosePlayer(canvas,data):
    startX = 300
    startY = 100
    data.startX,data.startY = startX,startY
    size = 40
    data.size = size
    if data.offMulti:
        string = "Your Turn"
        canvas.create_text(data.width/2,20,text=string,font = "Arial 20 bold",fill="White")
    canvas.create_text(data.width/2,60,text="Place Your Ships!",font = "Arial 16 bold",fill="White")
    drawGrid(canvas,startX,startY,size,data)
    if data.selected: drawSelectorChoose(canvas,data)
    if 0 not in data.placedList:
        canvas.create_image(60,70, anchor = NW,image = data.carrierhimage)
        canvas.create_text(140,95,text="Carrier",font="Arial 14 bold",fill="red")
    if 1 not in data.placedList:
        canvas.create_image(60,120, anchor = NW,image = data.battleshiphimage)
        canvas.create_text(140,145,text="Battleship",font="Arial 14 bold",fill="red")
    if 2 not in data.placedList:    
        canvas.create_image(60,170, anchor = NW,image = data.cruiserhimage)
        canvas.create_text(120,195,text="Cruiser",font="Arial 14 bold",fill="red")
    if 3 not in data.placedList:
        canvas.create_image(60,220, anchor = NW,image = data.subspacerhimage)
        canvas.create_text(120,245,text="Subspacer",font="Arial 14 bold",fill="red")
    if 4 not in data.placedList:
        canvas.create_image(60,270, anchor = NW,image = data.destroyerhimage)
        canvas.create_text(100,295,text="Destroyer",font="Arial 14 bold",fill="red")
    text = '''
    -> Move over the ships using your mouse. 
    -> Select the ship which you want to place on 
        the board by clicking on the ship.
    -> Once a ship is selected you will see a selected a
        rea on board. Use arrow keys
        to move around the board, space bar to rotate 
        and return to place.
    -> Click the ready button once you are done hiding
        your ships'''
    canvas.create_text(150, 370,text = text,font = "Arial 12 bold", fill = "white")
    canvas.create_rectangle(150,425,235,450,fill="white")
    canvas.create_text(190,435,text="Reset",fill="red",font="Arial 16 bold")
    canvas.create_rectangle(600,75,685,100,fill="white")
    canvas.create_text(640,85,text="Quit",fill="red",font="Arial 16 bold")
    canvas.create_rectangle(600,25,685,50,fill="white")
    canvas.create_text(640,35,text="Ready",fill="red",font="Arial 16 bold")
    if len(data.imageDictionary1) > 0:
        for image in data.imageDictionary1:
            shipSize = data.imageDictionary1[image][3]
            index = data.imageDictionary1[image][4]
            if index in data.placedList:
                x,y = getCellCoords(data,startX,startY,data.imageDictionary1[image][0],data.imageDictionary1[image][1],size,data.imageDictionary1[image][2],shipSize)
                canvas.create_image(x,y,image = image)


def drawSelectorPlay(canvas,data):
    if data.select:
        selector = data.selector
        x0,y0,x1,y1 = getBounds(selector[0],selector[1],data.startXPlayer1,data.startYPlayer1,data.size)
        canvas.create_rectangle(x0,y0,x1,y1,fill="yellow")

def findCoords(data,row,col,startx,starty,size):
    x = startx + (col+0.5) * size 
    y = starty + (row+0.5) * size
    return (x,y)


def drawPlayPlayer(canvas,data):
    startX = 10
    startY = 200
    data.startXPlayer1,data.startYPlayer1 = startX,startY
    size = 30
    data.size = size
    string = "Your Turn " if data.player1Turn else "Opponent's Turn"
    string2 = "Choose Where To Attack " if data.player1Turn else "Opponent is attacking"
    canvas.create_text(data.width/2,20,text=string,font = "Arial 20 bold",fill="White")
    canvas.create_text(data.width/2,60,text=string2,font = "Arial 16 bold",fill="White")
    drawGrid(canvas,startX,startY,size,data)
    startX = 400
    startY = 200
    data.startXPlayer2,data.startYPlayer2 = startX,startY
    drawGrid(canvas,startX,startY,size,data)
    canvas.create_rectangle(600,25,685,50,fill="white")
    canvas.create_text(640,35,text="Quit",fill="red",font="Arial 16 bold")
    if data.player1Turn:
        drawSelectorPlay(canvas,data)
    if data.hit:
        canvas.create_text(data.width/2+10,300,text="HIT!",font="Arial 28 bold",fill = "green")
        if data.player1Turn:
            x,y = findCoords(data,data.dupSelector1[0],data.dupSelector1[1],10,startY,size)
        else:
            x,y = findCoords(data,data.dupSelector2[0],data.dupSelector2[1],400,startY,size)
        canvas.create_oval(x-data.animRad,y-data.animRad,x+data.animRad,y+data.animRad,fill ="orange")
    if data.miss:
        canvas.create_text(data.width/2+10,300,text="MISS!",font="Arial 28 bold",fill = "red")
        if not data.player1Turn:
            x,y = findCoords(data,data.dupSelector1[0],data.dupSelector1[1],10,startY,size)
        else:
            x,y = findCoords(data,data.dupSelector2[0],data.dupSelector2[1],400,startY,size)
        canvas.create_oval(x-data.animRad,y-data.animRad,x+data.animRad,y+data.animRad,fill ="black")
    for image in data.imageDictionary2:
            shipSize = data.imageDictionary2[image][3]
            index = data.availShips.index(shipSize)
            x,y = getCellCoords(data,startX,startY,data.imageDictionary2[image][0],data.imageDictionary2[image][1],size,data.imageDictionary2[image][2],shipSize)
            canvas.create_image(x,y,image = image)

def drawOnMultiPlayer(canvas,data):
    if data.chooseMode and data.bothPlayers:
        drawChoosePlayer(canvas,data)
    elif data.playMode:
        drawPlayPlayer(canvas,data)
    else:
        canvas.create_text(data.width/2,100,text="Waiting For Other Player!",font="Arial 30 bold",fill = "white")

def redrawAll(canvas, data):
    if data.onMulti:
        drawOnMultiPlayer(canvas,data)


