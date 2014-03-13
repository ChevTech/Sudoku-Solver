#!/usr/bin/python

# Anton Stoytchev
# 04/08/2013

from Solver import Solver
import graphics

def getSudoku(boxes):
    sudokulist = []
    for box in boxes:
        sudokulist.append(box.get_text())
    
    for i in range (len(sudokulist)):
        if sudokulist[i] != '':
            sudokulist[i] = int(sudokulist[i])
    return sudokulist

def PrintPuzzle(boxes, board):
    for i in range(len(board)):
        boxes[i].set_text(board[i])

def ShiftBoxes(shift):
    if shift > 40:
        shift = shift + 5
    if shift > 120:
        shift = shift + 5
    return shift

if __name__ == '__main__':
    display = graphics.Display("white", 306, 320)        
    boxes = []
    solver = Solver()
    
    #make the Sudoku Board
    for x in range(0, 180, 20):
        x = ShiftBoxes(x)
        for y in range(0, 180, 20):
            y = ShiftBoxes(y)
            boxes.append(graphics.InputBox(2, "", y+75, x+50))
            
    #Generate a Black background for the dividing lines
    Rectangle = graphics.Rectangle('black', 65, 40, 255, 230)
        
    #make a Solve! Button
    SolvPuzzle = graphics.Button("Solve Puzzle", "white", 165, 250, 250, 270)
    
    #Display the board
    for box in boxes:
        display.add(box)
        
    #Display all objects
    display.add(SolvPuzzle)
    display.add(Rectangle)
    display.draw()
    
    #Event handler to slide clicked tiles
    def on_left_click(point):
        if SolvPuzzle.contains(point.x, point.y):
            sudokulist = getSudoku(boxes)
            solution = solver.solve(sudokulist)
            PrintPuzzle(boxes, solution)
    display.set_left_click_handler(on_left_click)
    
    while display.is_open():
        display.update(100)
            
    
    

    
    
