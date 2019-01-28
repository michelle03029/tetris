#################################################
# Colab5- Michelle Chen(mmchen), Myles Sherman (mbsherma)
# Melina Driscoll(msdrisco), Jac Council (jcouncil)
#################################################

import math
import string
import copy
import random

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

####################################
# customize these functions
####################################

from tkinter import *

def init(data):
    data.margin= 25
    data.width= 240
    data.height= 340
    data.rows= 15
    data.cols= 10
    data.cellSize= 20
    data.emptyColor= "blue"
    data.iPiece= [
        [  True,  True,  True,  True ]
    ]
    data.jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    data.lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    data.oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    data.sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    data.tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    data.zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    data.tetrisPieces= [ data.iPiece, data.jPiece, data.lPiece, 
    data.oPiece, data.sPiece, data.tPiece, data.zPiece ]
    data.tetrisPieceColors= [ "red", "yellow", "magenta", 
    "pink", "cyan", "green", "orange" ]
    data.fallingPieceCol= 0
    data.fallingPieceRow= 0
    data.fallingPieceCols= 0
    data.fallingPieceRows= 0
    data.fallingPiece= []
    data.isGameOver= False
    data.fullRows= 0
    starterBoard(data)
    newFallingPiece(data)
    
def starterBoard(data):
    # create basic board with empty cells
    data.board= []
    emptyColor= data.emptyColor
    for row in range(data.rows):
        result= []
        for col in range(data.cols):
            result.append(emptyColor)
        data.board += [result]

def keyPressed(event, data):
    if data.isGameOver==True: return
    # use keys to move piece or to 
    # start and restart game
    elif event.keysym == "Up":
        rotateFallingPiece(data)
    elif event.keysym == "Down":
        moveFallingPiece(data,1,0)
    elif event.keysym == "Left":
        moveFallingPiece(data,0,-1)
    elif event.keysym == "Right":
        moveFallingPiece(data,0,1)
    elif event.keysym == "space": 
        newFallingPiece(data)
    elif event.char == "r":
        init(data)
        
def mousePressed(event,data):
    pass
        
def playTetris():
    # for run function at end of code
    rows=15
    cols=10
    cellSize=20
    margin= 25
    width= (cols*cellSize)+(2*margin)
    height= (rows*cellSize)+(2*margin)
    run(width, height)

def timerFired(data):
    moveFallingPiece(data, +1, 0)
    if moveFallingPiece(data, +1, 0) == False:
        placeFallingPiece(data)
        # if falling piece automatically returns 
        # illegal, game over is true
        if fallingPieceIsLegal(data) == False:
            data.isGameOver= True
    
def drawCell(canvas, data, row, col, color):
    # draw cell for board function
    x0= col*data.cellSize+data.margin
    x1= (col+1)*data.cellSize+data.margin
    y0= row*data.cellSize+data.margin
    y1= (row+1)*data.cellSize+data.margin
    widthOutline= 4
    canvas.create_rectangle(x0, y0, x1, y1, fill= color, 
    outline= "black", width=widthOutline)
    
def drawBoard(canvas, data):
    # draw board with cells 
    for row in range(data.rows):
        for col in range(data.cols):
            color= data.board[row][col]
            drawCell(canvas, data, row, col, color)
            
def drawGameOver(canvas,data):
    # drawing "game over" message at
    # end of game
    canvas.create_text(data.width/2, data.height/2, text="Game Over!",
    fill="orange", font="Helvetica 30 bold")
            
def newFallingPiece(data):
    if data.isGameOver==False:
        # generate random tetris piece
        data.fallingPiece= data.tetrisPieces[random.randint(0, 
        len(data.tetrisPieces) - 1)]
        # generate random color for tetris piece
        data.fallingPieceColors= data.tetrisPieceColors[random.randint(0, 
        len(data.tetrisPieces) - 1)]
        data.fallingPieceRow= 0
        data.fallingPieceRows= len(data.fallingPiece)
        data.fallingPieceCols= len(data.fallingPiece[0])
        data.fallingPieceCol= (data.cols//2)- (data.fallingPieceCols//2)
    
def drawingFallingPiece(canvas, data):
    # draw the falling piece itself
    for row in range(len(data.fallingPiece)):
        rowList= data.fallingPiece[row]
        for col in range(len(rowList)):
            if data.fallingPiece[row][col]==True:
                # call draw cell draw the piece
                drawCell(canvas, data, data.fallingPieceRow+row, 
                data.fallingPieceCol+col, data.fallingPieceColors)
                
def moveFallingPiece(data, drow, dcol):
    if data.isGameOver==False:
        data.fallingPieceRow += drow
        data.fallingPieceCol += dcol
        if not(fallingPieceIsLegal(data)):
            # reset data or original values
            data.fallingPieceRow -= drow
            data.fallingPieceCol -= dcol
            return False
        return True
    
def fallingPieceIsLegal(data):
    for row in range(data.fallingPieceRows):
        for col in range(data.fallingPieceCols):
            # check falling piece is inside 
            # boundaries of the board
            if data.fallingPiece[row][col]==True:
                checkRow= data.fallingPieceRow+row
                checkCol= data.fallingPieceCol+col
                if (checkRow not in range(data.rows) or 
                checkCol not in range(data.cols)):
                    return False
                # color is emptyColor
                elif data.board[checkRow][checkCol] != data.emptyColor:
                    return False
    return True
    
def rotateFallingPiece(data):
    if data.isGameOver==False:
        oldNumRows= len(data.fallingPiece)
        oldNumCols= len(data.fallingPiece[0])
        oldRowLoc= data.fallingPieceRow 
        oldColLoc= data.fallingPieceCol
        oldPiece= copy.deepcopy(data.fallingPiece)
        newNumRows, newNumCols= oldNumCols, oldNumRows
        newRowLoc= oldRowLoc + oldNumRows//2 - oldNumCols//2
        newColLoc= oldColLoc + oldNumCols//2 - oldNumRows//2
        newPiece= []
        # create piece with None values
        for row in range(newNumRows):
            result= []
            for col in range(newNumCols):
                result.append(None)
            newPiece += [result]
        for row in range(oldNumRows):
            for col in range(oldNumCols):
                # set new variables
                newRow= (oldNumCols-1)-col
                newPiece[newRow][row] = oldPiece[row][col]
        data.fallingPiece= newPiece
        data.fallingPieceRow= newRowLoc
        data.fallingPieceCol= newColLoc
        data.fallingPieceRows= newNumRows
        data.fallingPieceCols= newNumCols
        if fallingPieceIsLegal(data)== False:
            # restore values 
            data.fallingPieceRows= oldNumRows
            data.fallingPieceCols= oldNumCols
            data.fallingPieceRow= oldRowLoc
            data.fallingPieceCol= oldColLoc
            data.fallingPiece= oldPiece
        
def placeFallingPiece(data):
    if data.isGameOver==False:
        for row in range(len(data.fallingPiece)):
            rowList= data.fallingPiece[row]
            for col in range(len(rowList)):
                # if the placement of falling piece 
                # call new variable to replace
                # falling piece colors
                if data.fallingPiece[row][col]==True:
                    newRow= data.fallingPieceRow+row
                    newCol= data.fallingPieceCol+col
                    data.board[newRow][newCol]= data.fallingPieceColors
        newFallingPiece(data)
        removeFullRows(data)
                
def removeFullRows(data):
    newBoard= []
    fullRows= 0
    for row in range(len(data.board)):
        # if there are empty blue cells in the row
        # append to an empty list to keep track
        if data.emptyColor in data.board[row]:
            newBoard.append(data.board[row])
        else: 
            fullRows += 1
    data.fullRows += (fullRows**2)
    for newRows in range(fullRows):
        # insert empty rows of blue cells to 
        # top of board
        newBoard.insert(0, [data.emptyColor]*data.cols)
    data.board= newBoard
    
def drawScore(canvas, data):
    # write score at top of board 
    canvas.create_text(data.width/2,data.margin/2, text="Score:"+ str(data.fullRows), 
    fill="blue", font="Helvetica 13 bold")
    
def redrawAll(canvas, data):
    # draw orange background
    canvas.create_rectangle(0, 0, data.width, data.height, fill= "orange")
    drawBoard(canvas, data)
    drawingFallingPiece(canvas, data)
    drawScore(canvas,data)
    # when game is over, draw game over message
    if data.isGameOver==True: drawGameOver(canvas,data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
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
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 800 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris()