from Tkinter import *
import string
import tkMessageBox
import tkSimpleDialog
import pickle
import os
import random
import main

def singleInit(data):
    data.rows = 10
    data.cols = 10
    data.player1Turn = True
    data.player1Ships = []
    data.player2Ships = []
    data.chooseMode = True
    data.playMode = False
    data.selector = [0,0]
    data.availShips = [5,4,3,3,2]
    data.shipSize = [5,4,3,3,2]
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
    data.aiTarget = []
    data.aiLag = 1000
    data.aiPrevHit = []
    data.aiHit = False
    data.aiShipDestroyed = False
    data.gotDirection = False
    data.miniTarget1 = []
    data.miniTarget2 = []
    data.firstDirection = False
    data.isDestroyer = False
    data.shipProbability = [[0]*data.cols for i in range(data.rows)]
    data.shots = 0
    data.prevLearning = [[0]*data.cols for i in range(data.rows)]
    data.aiCache = []
    data.notThisDir = False
    data.shots = 0
    getPrevLearning(data)
    data.streak = 0
    data.hard = False
    data.easy = False
    data.medium = False
    data.imageDictionary1 = {}
    askDifficulty(data)
    data.dupSelector1 = []
    data.dupSelector2 = []
    data.animRad = 15
    data.showAnimation = True
    data.hitList = []



def askDifficulty(data):
    title = "Game Difficulty"
    message = "What difficulty would you like? Press 'e' for easy, 'm' for medium and 'h' for hard"
    ans = tkSimpleDialog.askstring(title, message)
    if ans == 'e':
        data.easy = True
    elif ans == 'm':
        data.medium = True
    elif ans == 'h':
        data.hard = True
    else:
        title = "Error"
        message = "Your input was incorrect. Please try again!"
        tkMessageBox.showinfo(title,message)
        askDifficulty(data)




def getPrevLearning(data):
    try:
        shipListFile = open('Ships', 'r')
        sl = pickle.load(shipListFile)
        shipList = sl
    except:
        shipList = []
    if len(shipList) > 0:
        for l in shipList:
            for tup in l:
                row = tup[0]
                col = tup[1]
                data.prevLearning[row][col] += 1


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
            main.init(data.canvas,data)
    elif (600 <= event.x <= 685) and (25 <= event.y <= 50):
        if data.placed == 5:
            if tkMessageBox.askokcancel("Are you sure?", "You will not be able to change the location of your ships"):
                data.player1Turn = False
                data.placed = 0
                data.availShips = [5,4,3,3,2]
                hideAIShips(data)
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
            fileName ='s' + fileName + '.txt'
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
            aiTarget = data.aiTarget 
            aiPrevHit = data.aiPrevHit 
            aiHit = data.aiHit
            gotDirection = data.gotDirection
            miniTarget1 = data.miniTarget1 
            miniTarget2 = data.miniTarget2
            firstDirection = data.firstDirection 
            isDestroyer = data.isDestroyer
            shipProbability = data.shipProbability
            streak = data.streak
            saveList = [player1Turn,player1Ships,player2Ships,shipDictionary1,shipDictionary2,player1Guess,player2Guess,player2ShipList,
                        player1ShipList,aiTarget,aiPrevHit,aiHit,gotDirection,miniTarget1,miniTarget2,firstDirection,isDestroyer,shipProbability,streak]
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
        aiTarget = data.aiTarget 
        aiPrevHit = data.aiPrevHit 
        aiHit = data.aiHit
        gotDirection = data.gotDirection
        miniTarget1 = data.miniTarget1 
        miniTarget2 = data.miniTarget2
        firstDirection = data.firstDirection 
        isDestroyer = data.isDestroyer
        shipProbability = data.shipProbability
        streak = data.streak
        saveList = [player1Turn,player1Ships,player2Ships,shipDictionary1,shipDictionary2,player1Guess,player2Guess,player2ShipList,
                    player1ShipList,aiTarget,aiPrevHit,aiHit,gotDirection,miniTarget1,miniTarget2,firstDirection,isDestroyer,shipProbability,streak]
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
    elif  data.select and (10 <= event.x <= 310) and (200 <= event.y <= 500):
        row,col = getCell(data,event.x,event.y,10,200,30)
        data.selector[0] = row
        data.selector[1] = col

def doSingleMouse(event,data):
    if data.chooseMode:
        doMouseChoose(event,data)
    else:
        if data.player1Turn:
            doPlayMouse(event,data)

def mousePressed(event, data):
    doSingleMouse(event,data)



def hideAIShips(data):
    # first generates a cell randomly, then checks if the ship can be placed there given 
    # if it is vertical or not, and if it can be placed there, it places the ship there
    while data.placed < 5:
        for i in range(5):
            length = data.availShips[i]
            found = False
            L = []
            vertical = random.randint(0,1)
            if vertical == 0:
                while not found:
                    row = random.randint(0,9)
                    col = random.randint(0,9)
                    for j in range(length):
                        if (row,col+j) not in data.player2Ships and  ((col+j) <= 9):
                            L.append((row,col+j))
                            found = True
                        else:
                            found = False
                            L = []
                            break
            else:
                while not found:
                    row = random.randint(0,9)
                    col = random.randint(0,9)
                    for j in range(length):
                        if (row+j,col) not in data.player2Ships and  ((row+j) <= 9):
                            L.append((row+j,col))
                            found = True
                        else:
                            found = False
                            L = []
                            break
            data.player2Ships.extend(L)
            data.shipDictionary2[i].extend(L)
            data.placed += 1
    data.chooseMode = False
    data.playMode = True
    data.player1Turn = True



def doSingleChooseReturn(event,data):
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
            doSingleChooseReturn(event,data)

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

##############################################################################################################################
# The idea for the AI has been taken from onlne sources, but the algorithm and code is all mine.
##############################################################################################################################

def putShipOfSize(data,row,col,size):
    #this function counts the number of ways a ship of given size can be placed on a given cell 
    count = 0
    for i in range(size):
        firstCol = col - i 
        if firstCol < 0 or (row,firstCol) in data.player2Guess:
            break
        canPlace = True
        for i in range(size):
            newCol = firstCol + i
            if (row,newCol) in data.player2Guess or (newCol < 0) or (newCol > 9):
                canPlace = False
                break
        if canPlace:
            count += 1
    for i in range(size):
        firstRow = row - i 
        if firstRow < 0 or (firstRow,col) in data.player2Guess:
            break
        canPlace = True
        for i in range(size):
            newRow = firstRow + i
            if (newRow,col) in data.player2Guess or (newRow < 0) or (newRow > 9):
                canPlace = False
                break
        if canPlace:
            count += 1
    return count


def possibleShips(data,row,col):
    count = 0
    for size in data.shipSize:
        count += putShipOfSize(data,row,col,size)
    return count


def mostProbableCell(data):
    #first it generates the the list which will be used for the probability density AI
    for row in range(data.rows):
        for col in range(data.cols):
            if (row,col) in data.player2Guess:
                data.shipProbability[row][col] = 0
                continue
            count = possibleShips(data,row,col)
            data.shipProbability[row][col] = count
    #then it finds the cell with the highes probability and returns it
    maxCount = 0
    bestCells = []
    for row in range(data.rows):
        for col in range(data.cols):
            if data.shipProbability[row][col] > maxCount:
                bestCells = [(row,col)]
                maxCount = data.shipProbability[row][col]
            elif data.shipProbability[row][col] == maxCount:
                bestCells.append((row,col))
    if len(bestCells) == 1:
        return bestCells[0]
    else:
        if data.hard:
            # if user has chosen the hard mode, whenever there is a clash in probability, the ai will
            # create a list of the user's past placements of the ships and select the cell which has the highest
            # probability and has been selected by the user the most.
            most = 0
            row = 0
            col = 0
            bestCells2 = []
            for tup in bestCells:
                nRow = tup[0]
                nCol = tup[1]
                if data.prevLearning[nRow][nCol] > most:
                    bestCells2 = [(nRow,nCol)]
                elif data.prevLearning[nRow][nCol] == most:
                    bestCells2.append((nRow,nCol))
            if len(bestCells2) == 1:
                return bestCells2[0]
            else:
                index = random.randint(0,len(bestCells2)-1)
                return bestCells2[index]
        else:
            # if its not hard mode, the ai will choose randomly from the cells with highest probability 
            index = random.randint(0,len(bestCells)-1)
            return bestCells[index]


##############################################################################################################################
# I'm sorry for this next long function, but when I treid to trim it, it kept on crashing, so I have seperated it using comments,
# I hope that helps.
##############################################################################################################################


def doAIAttack(data):
    if len(data.aiTarget) == 0:
##############################################################################################################################
# This next part is the hunt mode for the AI
##############################################################################################################################
        found = False
        if not data.notThisDir: # if ships are not put together and the AI does not goes in a direction which is not of just one ship
        # the AI changes on the basis of the mode that the user has chosen
            if not data.easy:
                if data.hard:
                    if len(data.player2Guess) <= 60:
                        while not found:
                            if data.shots == 2 or data.shots == 4:
                                row = random.randint(0,9)
                                col = random.randint(0,9)
                            else:
                                (row,col) = mostProbableCell(data)
                            if ((row,col) not in data.player2Guess):
                                found = True
                                if data.shots == 5:
                                    data.shots = 0
                                else:
                                    data.shots += 1
                    else:
                        for tup in data.player1Ships:
                            if tup not in data.player2Guess:
                                row = tup[0]
                                col = tup[1]
                                break
                else:
                    if len(data.player2Guess) <= 75:
                        while not found:
                            if data.shots == 3:
                                row = random.randint(0,9)
                                col = random.randint(0,9)
                            else:
                                (row,col) = mostProbableCell(data)
                            if ((row,col) not in data.player2Guess):
                                found = True
                                if data.shots == 3:
                                    data.shots = 0
                                else:
                                    data.shots += 1
                    else:
                        for tup in data.player1Ships:
                            if tup not in data.player2Guess:
                                row = tup[0]
                                col = tup[1]
                                break
            else:
                while not found:
                    row = random.randint(0,9)
                    col = random.randint(0,9)
                    if ((row,col) not in data.player2Guess) and ((row + col) % 2 == 0):
                        found = True
        else:
            data.streak = 1
            row = data.hitList[0][0]
            col = data.hitList[0][1]
            data.hitList.pop(0)
            if len(data.hitList) == 0:
                data.notThisDir = False
            data.aiPrevHit = [row,col]
            if ((row+1,col) not in data.player2Guess) and ((row+1) < 10):
                data.aiTarget.append((row+1,col))
            if ((row-1,col) not in data.player2Guess) and ((row-1) > -1):
                data.aiTarget.append((row-1,col))
            if ((row,col+1) not in data.player2Guess) and ((col+1) < 10):
                data.aiTarget.append((row,col+1))
            if ((row,col-1) not in data.player2Guess) and ((col-1) > -1):
                data.aiTarget.append((row,col-1))
            return 
        tup = (row,col)
        data.dupSelector2 = [row,col]
        data.player2Guess.append(tup)
        if tup in data.player1Ships:
        ##############################################################################################################################
        # This next part is when the AI gets a hit in the hunt mode
        ##############################################################################################################################
            if GameOver(data,data.player2Guess):
                title = "Loss"
                message = "Computer Wins!"
                tkMessageBox.showinfo(title, message)
                main.init(data.canvas,data)
            if not data.notThisDir:
                data.hitList.append(tup)
            data.miss = False
            data.hit = True
            data.streak += 1
            for i in range(5):
                if i in data.player1ShipList:
                    if tup in data.shipDictionary1[i]:
                        data.shipDictionary1[i].remove(tup)
                        break
            for i in range(5):
                if i in data.player1ShipList:
                    if len(data.shipDictionary1[i]) == 0 and len(data.player1ShipList) > 1:
                        name = data.shipName[i]
                        title = "Oh No!"
                        message = "Your %s has been destroyed" %(name)
                        tkMessageBox.showinfo(title,message)
                        del data.shipDictionary1[i]
                        data.player1ShipList.remove(i)
                        data.aiShipDestroyed = True
                        break
            # it adds all the surrounding cells of the hit cell to a list if they haven't been guessed already
            data.aiPrevHit = [tup[0],tup[1]]
            if ((row+1,col) not in data.player2Guess) and ((row+1) < 10):
                data.aiTarget.append((row+1,col))
            if ((row-1,col) not in data.player2Guess) and ((row-1) > -1):
                data.aiTarget.append((row-1,col))
            if ((row,col+1) not in data.player2Guess) and ((col+1) < 10):
                data.aiTarget.append((row,col+1))
            if ((row,col-1) not in data.player2Guess) and ((col-1) > -1):
                data.aiTarget.append((row,col-1))
            if data.aiShipDestroyed:
                data.aiTarget = []
                data.aiShipDestroyed = False
                data.gotDirection = False
        else:
            #This is for when the AI missed in the hunt mode
            data.hit = False
            data.miss = True
            data.player1Turn = True
            data.hitList = []

    else:
##############################################################################################################################
# This next part is the target mode for the AI
##############################################################################################################################
        if data.gotDirection: # this is for when the AI knows the direction of a ship
            tup = data.aiTarget[0]
        else: # this is for when the AI doesn't know the direction of the ship
            #Here it calculates the maximum porbability for all the cells that can be the next part of the ship and attacks the cell
            # with the highest probability of having a ship
            for row in range(data.rows):
                for col in range(data.cols):
                    if (row,col) in data.player2Guess:
                        data.shipProbability[row][col] = 0
                        continue
                    count = possibleShips(data,row,col)
                    data.shipProbability[row][col] = count
            maxCount = 0
            bestCells = []
            for tup in data.aiTarget:
                row = tup[0]
                col = tup[1]
                if data.shipProbability[row][col] > maxCount:
                    bestCells = [(row,col)]
                    maxCount = data.shipProbability[row][col]
                elif data.shipProbability[row][col] == maxCount:
                    bestCells.append((row,col))
            if len(bestCells) == 1:
                tup = bestCells[0]
            else:
                index = random.randint(0,len(bestCells) - 1)
                tup = bestCells[index]
        data.dupSelector2 = [tup[0],tup[1]]
        if tup in data.player2Guess: # this is just a fail safe 
            data.aiTarget = []
            data.miniTarget2 = []
            data.miniTarget1 = []
            data.hit = False
            data.miss = False
            return 
        data.player2Guess.append(tup)
        if tup in data.player1Ships:
            ##############################################################################################################################
            # This next part is when the AI gets a hit in the target mode
            ##############################################################################################################################
            if GameOver(data,data.player2Guess):
                title = "Loss"
                message = "Computer Wins!"
                tkMessageBox.showinfo(title, message)
                addShipList(data)
                main.init(data.canvas,data)
            if not data.notThisDir:
                data.hitList.append(tup)
            data.miss = False
            data.hit = True
            data.streak += 1
            if not data.aiHit and not data.gotDirection:
                data.aiHit = True

            for i in range(5):
                if i in data.player1ShipList:
                    if tup in data.shipDictionary1[i]:
                        data.shipDictionary1[i].remove(tup)
                        break
            #Here it checks if it has destroyed the ship
            for i in range(5):
                if i in data.player1ShipList and len(data.player1ShipList) > 1:
                    if len(data.shipDictionary1[i]) == 0:
                        name = data.shipName[i]
                        title = "Oh No!"
                        message = "Your %s has been destroyed" %(name)
                        tkMessageBox.showinfo(title,message)
                        del data.shipDictionary1[i]
                        data.player1ShipList.remove(i)
                        data.aiShipDestroyed = True
                        if i == 4:
                            data.isDestroyer = True
                        size = data.availShips[i]
                        data.shipSize.remove(size)
                        if not data.easy:
                            #Here if it is not the easy mode, the ai will check if its current streak of hits is more than the size of the ship it has sunk
                            # and if it is it goes the other direction to kill the other ship.
                            if data.aiShipDestroyed:
                                size = data.availShips[i]
                                if data.streak > size and len(data.miniTarget2) > 0:
                                    data.aiShipDestroyed = False
                                    data.isDestroyer = False
                                    data.streak = 0
                                    if data.firstDirection:
                                        for tup in data.miniTarget1:
                                            data.aiTarget.remove(tup)
                                        data.miniTarget1 = []
                                        data.firstDirection = False
                                    elif len(data.miniTarget2) == 0 or not data.firstDirection:
                                        data.aiTarget = []
                                        shipList = data.player2Guess[::-1]
                                        found = 0
                                        cell1 = None
                                        cell2 = None
                                        for tup in shipList:
                                            if tup in data.player1Ships:
                                                found += 1
                                            if found == 1:
                                                cell1 = tup
                                            elif found == 2:
                                                cell2 = tup
                                                break
                                        rowDif = cell1[0] - cell2[0]
                                        colDif = cell1[1] - cell2[1]
                                        data.streak = 1
                                        if rowDif != 0:
                                            tup = (cell1[0] - (abs(rowDif)/rowDif) * (size),cell1[1])
                                        else:
                                            tup = (cell1[0],cell1[1] - (abs(colDif)/colDif) * (size))
                                        row,col = tup[0],tup[1]
                                        data.aiPrevHit = [row,col]
                                        if ((row+1,col) not in data.player2Guess) and ((row+1) < 10):
                                            data.aiTarget.append((row+1,col))
                                        if ((row-1,col) not in data.player2Guess) and ((row-1) > -1):
                                            data.aiTarget.append((row-1,col))
                                        if ((row,col+1) not in data.player2Guess) and ((col+1) < 10):
                                            data.aiTarget.append((row,col+1))
                                        if ((row,col-1) not in data.player2Guess) and ((col-1) > -1):
                                            data.aiTarget.append((row,col-1))
                                        data.aiHit = False
                                        data.gotDirection = False
                                        return 
                                    return
                        data.streak = 0
                        break

            if data.isDestroyer: # this is the special case when the ai destroys the ship of size 2
                data.aiTarget = []
                data.miniTarget1 = []
                data.miniTarget2 = []
                data.aiShipDestroyed = False
                data.gotDirection = False
                data.isDestroyer = False
                data.aiHit = False
                return
            if data.aiShipDestroyed: # this is for when the ai destroys a ship and its streak is the same as the size of the ship
                data.aiTarget = []
                data.miniTarget1 = []
                data.miniTarget2 = []
                if not data.notThisDir:
                    data.hitList = []
                data.aiShipDestroyed = False
                data.gotDirection = False
                data.aiHit = False
                return

            row = tup[0]
            col = tup[1]
            if data.aiHit:
            ##############################################################################################################################
            # This next part is when the AI previously had a hit, but did not have the direction, so it gets the direction from this next hit
            ##############################################################################################################################
                data.aiTarget.remove(tup)
                data.aiCache.extend(data.aiTarget)
                data.gotDirection = True
                data.aiTarget = []
                data.miniTarget1 =[] # the cells in one direction
                data.miniTarget2 =[] # the cells in the other direction
                rowDif = row - data.aiPrevHit[0]
                colDif = col - data.aiPrevHit[1]
                if rowDif != 0:
                    for i in range(1,8):
                        newRow = row + i*rowDif
                        if newRow > 9 or newRow < 0 or ((newRow,col) in data.player2Guess):
                            break
                        if ((newRow,col) not in data.player2Guess):
                            data.aiTarget.append((newRow,col))
                            data.miniTarget1.append((newRow,col))
                    for i in range(2,8):
                        newRow = row - i*rowDif
                        if newRow > 9 or newRow < 0 or ((newRow,col) in data.player2Guess):
                            break
                        if ((newRow,col) not in data.player2Guess):
                            data.aiTarget.append((newRow,col))
                            data.miniTarget2.append((newRow,col))
                else:
                    for i in range(1,8):
                        newCol = col + i*colDif
                        if newCol > 9 or newCol < 0 or ((row,newCol) in data.player2Guess):
                            break
                        if ((row,newCol) not in data.player2Guess):
                            data.aiTarget.append((row,newCol))
                            data.miniTarget1.append((row,newCol))
                    for i in range(2,8):
                        newCol = col - i*colDif
                        if newCol > 9 or newCol < 0 or ((row,newCol) in data.player2Guess):
                            break
                        if ((row,newCol) not in data.player2Guess):
                            data.aiTarget.append((row,newCol))
                            data.miniTarget2.append((row,newCol))
                data.aiHit = False
                data.firstDirection = True
                return 
            if not data.gotDirection:
                data.aiTarget = []
                if ((row+1,col) not in data.player2Guess) and ((row+1) <= 9):
                    data.aiTarget.append((row+1,col))
                if ((row-1,col) not in data.player2Guess) and ((row-1) >= 0):
                    data.aiTarget.append((row-1,col))
                if ((row,col+1) not in data.player2Guess) and ((col+1) <= 9):
                    data.aiTarget.append((row,col+1))
                if ((row,col-1) not in data.player2Guess) and ((col-1) >= 0):
                    data.aiTarget.append((row,col-1))
            else:
                if len(data.miniTarget1) == 0:
                    data.firstDirection = False
                data.aiTarget.remove(tup)
                if data.firstDirection:
                    data.miniTarget1.remove(tup)
                else:
                    if len(data.miniTarget2) != 0:
                        data.miniTarget2.remove(tup)

        else: # this is for when the ai misses in target mode
            data.hit = False
            data.miss = True
            data.player1Turn = True
            if data.gotDirection:
                if data.firstDirection:
                    for tup in data.miniTarget1:
                        data.aiTarget.remove(tup)
                    data.miniTarget1 = []
                    data.firstDirection = False
                    if len(data.miniTarget2) == 0:
                        data.notThisDir = True
                        data.aiTarget = []
                        data.miniTarget1 = []
                        data.miniTarget2 = []
                        data.gotDirection = False
                        data.aiHit = False
                else:
                    data.notThisDir = True
                    data.aiTarget = []
                    data.miniTarget1 = []
                    data.miniTarget2 = []
                    data.gotDirection = False
                    data.aiHit = False
                    
            else:
              data.aiTarget.remove(tup)

           

def addShipList(data): # here after the game ends the ai adds the ship placemencts of the user to a file
    try:
        shipListFile = open('Ships', 'r')
        sl = pickle.load(shipListFile)
        shipList = sl
    except:
        shipList = []
    shipList.append(data.player1Ships)
    fileName = "Ships"
    listOfShips = open(fileName, 'w')
    pickle.dump(shipList, listOfShips)


def doSinglePlayReturn(event,data):
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
                message = "You Win!!"
                tkMessageBox.showinfo(title, message)
                addShipList(data)
                main.init(data.canvas,data)
            data.dupSelector1 = data.selector
            data.select = False
            if (data.selector[0],data.selector[1]) not in data.player2Ships:
                data.player1Turn = False
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
        doSinglePlayReturn(event,data)


def doKeySingle(event,data):
    if data.chooseMode:
        doKeyChooseMode(event,data)
    else:
        if data.player1Turn:
            doKeyPlayMode(event,data)

def keyPressed(event, data):
    doKeySingle(event,data)


def timerFired(data):
    if data.miss or data.hit:
        if data.timer > 0:  
            data.showAnimation = True
            data.timer -= data.timerDelay
            data.animRad -= 1.5
        else:
            data.miss = False
            data.hit = False
            data.timer = 1000
            data.animRad = 15
            data.showAnimation = False
            data.select = True
    if data.playMode and not data.player1Turn and not data.showAnimation:
        if data.aiLag > 0:
            data.aiLag -= data.timerDelay
        else:
            doAIAttack(data)
            data.aiLag = 1000

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
            if data.singlePlay:
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
                canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=3)
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
    if data.chooseMode:
        if shipSize == 5 or shipSize == 3:
            margin = 25
    elif data.playMode:
        if shipSize == 5:
            margin = 20
        elif shipSize == 3:
            margin = 15
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
    -> Once a ship is selected you will see a selected a
        red on board. Use arrow keys
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
    string = "Your Turn " if data.player1Turn else "Computer's Turn"
    canvas.create_text(data.width/2,20,text=string,font = "Arial 20 bold",fill="White")
    string2 = "Choose Where To Attack!" if data.player1Turn else "Computer is attacking!"
    canvas.create_text(data.width/2,60,text=string2,font = "Arial 16 bold",fill="White")
    drawGrid(canvas,startX,startY,size,data)
    startX = 400
    startY = 200
    data.startXPlayer2,data.startYPlayer2 = startX,startY
    drawGrid(canvas,startX,startY,size,data)
    canvas.create_rectangle(590,25,685,50,fill="white")
    canvas.create_text(640,35,text="Save Game",fill="red",font="Arial 16 bold")
    canvas.create_rectangle(600,75,685,100,fill="white")
    canvas.create_text(640,85,text="Quit",fill="red",font="Arial 16 bold")
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

def drawSinglePlayer(canvas,data):
    if data.chooseMode:
        drawChoosePlayer(canvas,data)
    elif data.playMode:
        drawPlayPlayer(canvas,data)
   
def redrawAll(canvas, data):
    drawSinglePlayer(canvas,data)


