from Tkinter import *
import string
import tkMessageBox
import tkSimpleDialog
import pickle
import os
import random
import main


def multiInit(data):
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
        data.shipDictionary2[i] = []
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
    data.imageDictionary1 = {}
    data.imageDictionary2 = {}
    data.dupSelector1 = []
    data.dupSelector2 = []
    data.animRad = 20


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
        if data.player1Turn:
            data.imageDictionary1 = {}
        else:
            data.imageDictionary2 = {}
    elif (600 <= event.x <= 685) and (75 <= event.y <= 100):
        if tkMessageBox.askokcancel("Are you sure?", "You will be sent to the main screen!"):
            main.init(data.canvas,data)
    elif (600 <= event.x <= 685) and (25 <= event.y <= 50):
        if data.placed == 5:
            if tkMessageBox.askokcancel("Are you sure?", "You will not be able to change the location of your ships"):
                if data.player1Turn:
                    data.player1Turn = False
                    data.player2Turn = True
                    data.placedList = []
                    data.placed = 0
                else:
                    data.chooseMode = False
                    data.playMode = True
                    data.player1Turn = True
                    data.player2Turn = False
                    data.select = True
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

##############################################################################################################################
# The load Game and save game features using pickle have been learned from the internet, hte code is all mine but it was learned 
# from the internet and the architecture for it is not mine.
##############################################################################################################################


def getFileName(data):
    title = "Save Game"
    message = "What name would you like to save the file by?"
    fileName = tkSimpleDialog.askstring(title, message)
    mistake = 0
    if fileName != None:
        for char in fileName:
            if (char in string.punctuation) or (char in string.whitespace):
                mistake += 1
        if mistake == 0:
            fileName = fileName.lower()
            fileName ='m' + fileName + '.txt'
            return fileName
        else:
            title = "Error"
            message = "No special character or spaces allowed in file name"
            tkMessageBox.showinfo(title, message)

def saveGame(data):
    fileName = getFileName(data)
    if fileName == None:
        title = "Error"
        message = "It seems you have not typed any names"
        tkMessageBox.showinfo(title, message)
    elif os.path.exists(fileName):
        title = "Already Exists"
        message = "It seems there is already a file of that name."
        tkMessageBox.showinfo(title, message)
        if tkMessageBox.askokcancel("Overwirte","Would you like to overwite the saved file?"):
            player1Turn = data.player1Turn 
            player1Ships = data.player1Ships 
            player2Ships = data.player2Ships 
            shipDictionary1 = data.shipDictionary1 
            shipDictionary2 = data.shipDictionary2 
            player1Guess = data.player1Guess 
            player2Guess = data.player2Guess
            player2ShipList = data.player2ShipList 
            player1ShipList = data.player1ShipList
            saveList = [player1Turn,player1Ships,player2Ships,shipDictionary1,shipDictionary2,player1Guess,player2Guess,player2ShipList,player1ShipList]
            saveFile = open(fileName, 'w')
            pickle.dump(saveList, saveFile)
            saveFile.close()
    else:
        player1Turn = data.player1Turn 
        player1Ships = data.player1Ships 
        player2Ships = data.player2Ships 
        shipDictionary1 = data.shipDictionary1 
        shipDictionary2 = data.shipDictionary2 
        player1Guess = data.player1Guess 
        player2Guess = data.player2Guess
        player2ShipList = data.player2ShipList 
        player1ShipList = data.player1ShipList
        saveList = [player1Turn,player1Ships,player2Ships,shipDictionary1,shipDictionary2,player1Guess,player2Guess,player2ShipList,player1ShipList]
        saveFile = open(fileName, 'w')
        pickle.dump(saveList, saveFile)
        saveFile.close()


def getCell(data,x,y,startX,startY,size):
    row = (y - startY) / size
    col = (x - startX) / size
    return (row,col)

def doPlayMouse(event,data): 
    if (600 <= event.x <= 685) and (75 <= event.y <= 100):
        if tkMessageBox.askokcancel("Are you sure?", "You will be sent to the main screen!"):
            main.init(data.canvas,data)
    elif (590 <= event.x <= 685) and (25 <= event.y <= 50):
        saveGame(data)
    elif  (175 <= event.x <= 575) and (100 <= event.y <= 500):
        row,col = getCell(data,event.x,event.y,175,100,40)
        data.selector[0] = row
        data.selector[1] = col

def doMultiMouse(event,data):
    if data.chooseMode:
        doMouseChoose(event,data)
    else:
        doPlayMouse(event,data)

def mousePressed(event, data):
    doMultiMouse(event,data)


def doOffMultiChooseReturn(event,data):
    if event.keysym == "Return":
        L = []
        addToList = True
        if data.player1Turn:
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
                if data.vertical:
                    data.imageDictionary1[data.shipImages[data.shipIndex][1]] = [data.selector[0],data.selector[1],1,data.availShips[data.shipIndex],data.shipIndex]
                else:
                    data.imageDictionary1[data.shipImages[data.shipIndex][0]] = [data.selector[0],data.selector[1],0,data.availShips[data.shipIndex],data.shipIndex]
                data.selector[0],data.selector[1] = 0,0
                data.placed += 1
                data.placedList.append(data.shipIndex)
                data.shipDictionary1[data.shipIndex].extend(L)
                data.selected = False

        else:
            for i in range(data.availShips[data.shipIndex]):
                if data.vertical:
                    tup = (data.selector[0]+i,data.selector[1])
                    if tup in data.player2Ships:
                        title = "Error"
                        message = "Ship Already There"
                        tkMessageBox.showinfo(title, message)
                        addToList = False
                        break
                else:
                    tup = (data.selector[0],data.selector[1]+i)
                    if tup in data.player2Ships:
                        title = "Error"
                        message = "Ship Already There"
                        tkMessageBox.showinfo(title, message)
                        addToList = False
                        break
                L.append(tup)
            if addToList:
                data.player2Ships.extend(L)
                if data.vertical:
                    data.imageDictionary2[data.shipImages[data.shipIndex][1]] = [data.selector[0],data.selector[1],1,data.availShips[data.shipIndex]]
                else:
                    data.imageDictionary2[data.shipImages[data.shipIndex][0]] = [data.selector[0],data.selector[1],0,data.availShips[data.shipIndex]]
                data.selector[0],data.selector[1] = 0,0
                data.placedList.append(data.shipIndex)
                data.shipDictionary2[data.shipIndex].extend(L)
                data.selected = False
                data.placed += 1
                data.select = True


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
            if data.offMulti:
                doOffMultiChooseReturn(event,data)


def GameOver(data,L):
    if data.player1Turn:
        for tup in data.player2Ships:
            if tup not in L:
                return False
    else:
        for tup in data.player1Ships:
            if tup not in L:
                return False
    return True

def doOffKeyPlayReturn(event,data):
    if event.keysym == "Return":
        canvas = data.canvas
        if data.player1Turn:
            if (data.selector[0],data.selector[1]) in data.player1Guess:
                title = "Error"
                message = "You've Already Attacked There"
                tkMessageBox.showinfo(title, message)
                return
            data.player1Guess.append((data.selector[0],data.selector[1]))
            if GameOver(data,data.player1Guess):
                title = "Victory"
                message = "Player 1 Wins!"
                tkMessageBox.showinfo(title, message)
                main.init(canvas,data)
            data.dupSelector1 = data.selector
            data.select = False
            if (data.selector[0],data.selector[1]) not in data.player2Ships:
                data.hit = False
                data.miss = True
                data.selector = [0,0]
            else:
                data.miss = False
                data.hit = True
                tup = (data.selector[0],data.selector[1])
                for i in range(5):
                    if i in data.player2ShipList:
                        if tup in data.shipDictionary2[i]:
                            data.shipDictionary2[i].remove(tup)
                            break
                for i in range(5):
                    if i in data.player2ShipList and len(data.player2ShipList) > 1:
                        if len(data.shipDictionary2[i]) == 0:
                            name = data.shipName[i]
                            title = "Congratulations!"
                            message = "You have destroyed the enemy's %s" %(name)
                            tkMessageBox.showinfo(title,message)
                            del data.shipDictionary2[i]
                            data.player2ShipList.remove(i)
                            break
        else:
            if (data.selector[0],data.selector[1]) in data.player2Guess:
                title = "Error"
                message = "You've Already Attacked There"
                tkMessageBox.showinfo(title, message)
                return
            data.player2Guess.append((data.selector[0],data.selector[1]))
            if GameOver(data,data.player2Guess):
                title = "Victory"
                message = "Player 2 Wins!"
                tkMessageBox.showinfo(title, message)
                main.init(canvas,data)
            data.dupSelector2 = data.selector
            data.select = False
            if (data.selector[0],data.selector[1]) not in data.player1Ships:
                data.hit = False
                data.miss = True
                data.selector = [0,0]
            else:
                data.miss = False
                data.hit = True
                tup = (data.selector[0],data.selector[1])
                for i in range(5):
                    if i in data.player1ShipList:
                        if tup in data.shipDictionary1[i]:
                            data.shipDictionary1[i].remove(tup)
                            break
                for i in range(5):
                    if i in data.player1ShipList and len(data.player1ShipList) > 1:
                        if len(data.shipDictionary1[i]) == 0:
                            name = data.shipName[i]
                            title = "Congratulations!"
                            message = "You have destroyed the enemy's %s" %(name)
                            tkMessageBox.showinfo(title,message)
                            del data.shipDictionary1[i]
                            data.player1ShipList.remove(i)
                            break



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
        if data.offMulti:
            doOffKeyPlayReturn(event,data)
    



def doKeyOffMulti(event,data):
    if data.chooseMode:
        doKeyChooseMode(event,data)
    else:
        doKeyPlayMode(event,data)

def keyPressed(event, data):
    if data.offMulti:
        doKeyOffMulti(event,data)



def timerFired(data):
    if data.miss or data.hit:
        if data.timer > 0:  
            data.timer -= data.timerDelay
            data.animRad -= 2
        else:
            if data.miss:
                data.player1Turn = not data.player1Turn
            data.miss = False
            data.hit = False
            data.timer = 1000
            data.animRad = 20
            data.select = True



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
            if data.offMulti:
                if data.chooseMode:
                    if data.player1Turn:
                        color = "lightCyan" 
                    elif data.player2Turn:
                        color = "ivory"
                elif data.playMode:
                    if data.player1Turn:
                        if (row,col) in data.player1Guess and (row,col) in data.player2Ships: color = "green"
                        elif (row,col) in data.player1Guess : color = "red"
                        else: color = "ivory"
                    else:
                        if (row,col) in data.player2Guess and (row,col) in data.player1Ships: color = "green"
                        elif (row,col) in data.player2Guess : color = "red"
                        else: color = "lightCyan"
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
        string = "Player 1 Turn " if data.player1Turn else "Player 2 Turn"
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
    -> Once a ship is selected you will see a selected 
        region on board. Use arrow keys or click on a cell
        to move around the board, space bar to rotate the
        ship and enter to place the ship.
    -> Click the ready button once you are done hiding
        your ships'''
    canvas.create_text(150, 370,text = text,font = "Arial 12 bold", fill = "white")
    canvas.create_rectangle(150,425,235,450,fill="white")
    canvas.create_text(190,435,text="Reset",fill="red",font="Arial 16 bold")
    canvas.create_rectangle(600,75,685,100,fill="white")
    canvas.create_text(640,85,text="Quit",fill="red",font="Arial 16 bold")
    canvas.create_rectangle(600,25,685,50,fill="white")
    canvas.create_text(640,35,text="Ready",fill="red",font="Arial 16 bold")
    if data.player1Turn:
        if len(data.imageDictionary1) > 0:
            for image in data.imageDictionary1:
                shipSize = data.imageDictionary1[image][3]
                index = data.imageDictionary1[image][4]
                if index in data.placedList:
                    x,y = getCellCoords(data,startX,startY,data.imageDictionary1[image][0],data.imageDictionary1[image][1],size,data.imageDictionary1[image][2],shipSize)
                    canvas.create_image(x,y,image = image)
    else:
        if len(data.imageDictionary2) > 0:
            for image in data.imageDictionary2:
                shipSize = data.imageDictionary2[image][3]
                index = data.imageDictionary1[image][4]
                if index in data.placedList:
                    x,y = getCellCoords(data,startX,startY,data.imageDictionary2[image][0],data.imageDictionary2[image][1],size,data.imageDictionary2[image][2],shipSize)
                    canvas.create_image(x,y,image = image)



def drawSelectorPlay(canvas,data):
    if data.select:
        selector = data.selector
        x0,y0,x1,y1 = getBounds(selector[0],selector[1],data.startX,data.startY,data.size)
        canvas.create_rectangle(x0,y0,x1,y1,fill="yellow")

def findCoords(data,row,col,startx,starty,size):
    x = startx + (col+0.5) * size 
    y = starty + (row+0.5) * size
    return (x,y)

def drawPlayPlayer(canvas,data):
    startX = 175
    startY = 100
    data.startX,data.startY = startX,startY
    size = 40
    data.size = size
    string = "Player 1 Turn " if data.player1Turn else "Player 2 Turn"
    canvas.create_text(data.width/2,20,text=string,font = "Arial 20 bold",fill="White")
    canvas.create_text(data.width/2,60,text="Choose Where To Attack!",font = "Arial 16 bold",fill="White")
    drawGrid(canvas,startX,startY,size,data)
    drawSelectorPlay(canvas,data)
    canvas.create_rectangle(590,25,685,50,fill="white")
    canvas.create_text(640,35,text="Save Game",fill="red",font="Arial 16 bold")
    canvas.create_rectangle(600,75,685,100,fill="white")
    canvas.create_text(640,85,text="Quit",fill="red",font="Arial 16 bold")
    if data.hit:
        canvas.create_text(75,250,text="HIT!",font="Arial 28 bold",fill = "green")
        if data.player1Turn:
            x,y = findCoords(data,data.dupSelector1[0],data.dupSelector1[1],startX,startY,size)
        else:
            x,y = findCoords(data,data.dupSelector2[0],data.dupSelector2[1],startX,startY,size)
        canvas.create_oval(x-data.animRad,y-data.animRad,x+data.animRad,y+data.animRad,fill ="orange")
    if data.miss:
        canvas.create_text(75,250,text="MISS!",font="Arial 28 bold",fill = "red")
        if data.player1Turn:
            x,y = findCoords(data,data.dupSelector1[0],data.dupSelector1[1],startX,startY,size)
        else:
            x,y = findCoords(data,data.dupSelector2[0],data.dupSelector2[1],startX,startY,size)
        canvas.create_oval(x-data.animRad,y-data.animRad,x+data.animRad,y+data.animRad,fill ="black")

def drawOffMultiplayer(canvas,data):
    if data.chooseMode:
        drawChoosePlayer(canvas,data)
    else:
        drawPlayPlayer(canvas,data)

def redrawAll(canvas, data):
    if data.offMulti:
        drawOffMultiplayer(canvas,data)



