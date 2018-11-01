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
import offline
import online
import single


##############################################################################################################################
# The MVC architecture is not mine, it has been taken from the 112 website and has been modified to suit my needs
##############################################################################################################################

def init(canvas,data):
    data.splashMode = True
    data.offMulti = False
    data.singlePlay = False
    data.onMulti = False
    data.instructions = False
    data.canvas = canvas
    buttons = []
    def f():instructInit(data)
    instructions = Button(canvas,text = "Instructions", font = "Times 25 bold", cursor = "target",command = f)
    def i():
        data.splashMode = False
        data.singlePlay = True
        single.singleInit(data)
    playGame1 = Button( canvas, text = "Play Single Player ", font = "Times 25 bold", cursor = "target",command = i)
    def h():
        data.splashMode = False
        data.offMulti = True
        offline.multiInit(data)
    playGame2 = Button(canvas, text = "Play Offline Multiplayer ", font = "Times 25 bold", cursor = "target",command=h)
    def k():
        data.splashMode = False
        data.onMulti = True
        online.multiInit(data)
    playGame3 = Button(canvas, text = "Play Online Multiplayer ", font = "Times 25 bold", cursor = "target",command = k)
    def j():
        loadTheGame(data)
    loadGame = Button(canvas, text = "Load Game", font = "Times 25 bold", cursor = "target",command = j)
    buttons.extend([instructions,playGame1,playGame2,playGame3,loadGame])
    def g(): init(canvas,data)
    splashBack = Button(canvas,text="Back",font = "Times 25 bold", cursor = "target",command = g)
    data.splashButtons = buttons
    data.splashBack = splashBack
    loadImages(data)

##############################################################################################################################
# The images for the battleship ships have been taken from the internet and the code to use images has been learned from the 
# 112 website.
##############################################################################################################################

def loadImages(data):
    data.carrierhimage = PhotoImage(file="Carrierh.gif")
    data.battleshiphimage = PhotoImage(file="Battleshiph.gif")
    data.cruiserhimage = PhotoImage(file="Cruiserh.gif")
    data.subspacerhimage = PhotoImage(file="Subspacerh.gif")
    data.destroyerhimage = PhotoImage(file="Destroyerh.gif")
    data.carriervimage = PhotoImage(file="Carrierv.gif")
    data.battleshipvimage = PhotoImage(file="Battleshipv.gif")
    data.cruiservimage = PhotoImage(file="Cruiserv.gif")
    data.subspacervimage = PhotoImage(file="Subspacerv.gif")
    data.destroyervimage = PhotoImage(file="Destroyerv.gif")
    data.shipImages = {}
    data.shipImages[0] = [data.carrierhimage,data.carriervimage]
    data.shipImages[1] = [data.battleshiphimage,data.battleshipvimage]
    data.shipImages[2] = [data.cruiserhimage,data.cruiservimage]
    data.shipImages[3] = [data.subspacerhimage,data.subspacervimage]
    data.shipImages[4] = [data.destroyerhimage,data.destroyervimage]
    data.smallCarrierhimage = PhotoImage(file="smallCarrierh.gif")
    data.smallCarriervimage = PhotoImage(file="smallCarrierv.gif")
    data.smallBattleshiphimage = PhotoImage(file="smallBattleshiph.gif")
    data.smallBattleshipvimage = PhotoImage(file="smallBattleshipv.gif")
    data.smallCruiserhimage = PhotoImage(file="smallCruiserh.gif")
    data.smallCruiservimage = PhotoImage(file="smallCruiserv.gif")
    data.smallSubspacerhimage = PhotoImage(file="smallSubspacerh.gif")
    data.smallSubspacervimage = PhotoImage(file="smallSubspacerv.gif")
    data.smallDestroyerhimage = PhotoImage(file="smallDestroyerh.gif")
    data.smallDestroyervimage = PhotoImage(file="smallDestroyerv.gif")
    data.smallShipImages = {}
    data.smallShipImages[0] = [data.smallCarrierhimage,data.smallCarriervimage]
    data.smallShipImages[1] = [data.smallBattleshiphimage, data.smallBattleshipvimage]
    data.smallShipImages[2] = [data.smallCruiserhimage,data.smallCruiservimage]
    data.smallShipImages[3] = [data.smallSubspacerhimage,data.smallSubspacervimage]
    data.smallShipImages[4] = [data.smallDestroyerhimage,data.smallDestroyervimage]


##############################################################################################################################
# The load Game and save game features using pickle have been learned from the internet, hte code is all mine but it was learned 
# from the internet and the architecture for it is not mine.
##############################################################################################################################

def loadMultiGame(data):
    title = "Load Game"
    message = "Enter the name for your save file"
    fileName = tkSimpleDialog.askstring(title, message)
    if fileName == None:
        init(data.canvas,data)
    else:
        fileName = fileName.lower()
        fileName = 'm' + fileName
        if fileName == 'm':
            title = "Error"
            message = "No file name given!"
            tkMessageBox.showinfo(title, message)
            init(data.canvas,data)
        else:
            fileName += '.txt'
            if os.path.exists(fileName) == False:
                title = "Error"
                message = "No such file exists!"
                tkMessageBox.showinfo(title, message)
                init(data.canvas,data)
            else:
                loadFile = open(fileName, 'r')
                saveList = pickle.load(loadFile)
                data.splashMode = False
                data.offMulti = True
                data.select = True
                offline.multiInit(data)
                data.chooseMode = False
                data.playMode = True
                data.player1Turn = saveList[0]
                data.player1Ships = saveList[1]
                data.player2Ships = saveList[2]
                data.shipDictionary1 = saveList[3]
                data.shipDictionary2 = saveList[4]
                data.player1Guess = saveList[5]
                data.player2Guess = saveList[6]
                data.player2ShipList = saveList[7]
                data.player1ShipList = saveList[8]


def loadSingleGame(data):
    title = "Load Game"
    message = "Enter the name for your save file"
    fileName = tkSimpleDialog.askstring(title, message)
    if fileName == None:
        init(data.canvas,data)
    else:
        fileName = fileName.lower()
        fileName = 's' + fileName
        if fileName == 's':
            title = "Error"
            message = "No file name given!"
            tkMessageBox.showinfo(title, message)
            init(data.canvas,data)
        else:
            fileName += '.txt'
            if os.path.exists(fileName) == False:
                title = "Error"
                message = "No such file exists!"
                tkMessageBox.showinfo(title, message)
                init(data.canvas,data)
            else:
                loadFile = open(fileName, 'r')
                saveList = pickle.load(loadFile)
                data.splashMode = False
                data.singlePlay = True
                data.select = True
                single.singleInit(data)
                data.chooseMode = False
                data.playMode = True
                data.player1Turn = saveList[0]
                data.player1Ships = saveList[1]
                data.player2Ships = saveList[2]
                data.shipDictionary1 = saveList[3]
                data.shipDictionary2 = saveList[4]
                data.player1Guess = saveList[5]
                data.player2Guess = saveList[6]
                data.player2ShipList = saveList[7]
                data.player1ShipList = saveList[8]
                data.aiTarget = saveList[9]
                data.aiPrevHit = saveList[10]
                data.aiHit = saveList[11]
                data.gotDirection = saveList[12]
                data.miniTarget1 = saveList[13]
                data.miniTarget2 = saveList[14]
                data.firstDirection = saveList[15]
                data.isDestroyer = saveList[16]
                data.shipProbability = saveList[17]
                data.streak = saveList[18]

def loadTheGame(data):
    mode = tkMessageBox.askquestion("Game Mode", "Was your game mode Multiplayer?")
    if mode == 'yes':
        loadMultiGame(data)
    else:
        loadSingleGame(data)

def instructInit(data):
    data.splashMode = False
    data.instructions = True


def drawInstructions(canvas,data):
    text = '''
    -> There are three modes from which you can choose - Single Player, Offline 
        Multiplayer and online Multiplayer. 
    -> For online Multiplayer, before clicking on the button, you must open the server
        file that has also been provided.
    -> The game is simple battleship, first you must hide your ships and then guess
        the location of your opponent's ship. While playing you can use both arrow
        keys and mouse to move, and enter to give a selection.
    -> For each hit, you will see a green hit message and a green cell at which
        you got a hit. For each miss you will see a red miss message and a red
        cell at which you got a hit.
    -> If you hit, you will get to guess again until you miss.
    -> You can save the game and then quit to go to the menu and then 
         load your saved game to continue if your game was offline.
    -> For a challenging game against the computer, hide your ships far from each
        other
    -> Click on back to go back to the menu.'''
    canvas.create_text(data.width/2, 25, text = "Instructions", font = "Times 22 bold", fill = 'yellow')
    canvas.create_text(350, 200, text = text, font = "Times 18 bold", fill = 'yellow')
    canvas.create_window(data.width/3,data.height*7/8,window=data.splashBack,anchor=CENTER)

def keyPressed(event,data):
    if data.offMulti:
        offline.keyPressed(event,data)
    elif data.onMulti:
        online.keyPressed(event,data)
    elif data.singlePlay:
        single.keyPressed(event,data)

def mousePressed(event,data):
    if data.offMulti:
        offline.mousePressed(event,data)
    elif data.onMulti:
        online.mousePressed(event,data)
    elif data.singlePlay:
        single.mousePressed(event,data)

def timerFired(data):
    if data.onMulti:
        online.timerFired(data)
    elif data.offMulti:
        offline.timerFired(data)
    elif data.singlePlay:
        single.timerFired(data)

def drawSplashMode(canvas,data):
    x = data.width/2
    canvas.create_text(x,50,anchor=CENTER,text="Battleship 112!!!",font="Arial 30 bold underline",fill="yellow")
    y = 100
    buttons = data.splashButtons
    for button in buttons:
        canvas.create_window(x, y, window = button, anchor = CENTER)
        y += 80

##############################################################################################################################
# The background image has been taken from the internet.
##############################################################################################################################

def redrawAll(canvas,data):
    canvas.create_image(0,0, anchor = NW,image = data.image)
    if data.splashMode:
        drawSplashMode(canvas,data)
    elif data.instructions:
        drawInstructions(canvas,data)
    elif data.offMulti: 
        offline.redrawAll(canvas,data)
    elif data.onMulti:
        online.redrawAll(canvas,data)
    elif data.singlePlay:
        single.redrawAll(canvas,data)


def run(width=500, height=500,serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        if not data.splashMode and not data.instructions:
            redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    root = Tk()
    root.title("Battleship 112!!!")
    root.resizable(width = False, height = False)
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(canvas,data)
    bgImage = PhotoImage(file="space_background.gif")
    data.image = bgImage
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()  


def main():
    run(700, 500)

if __name__ == "__main__":
    main()