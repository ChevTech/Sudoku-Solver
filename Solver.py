# A class that represents a Sudoku Solver Algorithm 
import sys

class Solver(object):
    
    def __init__(self):    
        self.mistakes = 0
        self.assigned  = 0
        
    def solve(self, board):
        rows    = self.getRows(board) # get the rows of the board
        columns = self.getColumns(rows) # get the columns of the board
        boxes   = self.getBoxes(rows) # get the boxes
        
        #Solve the board
        if self.solver(rows, columns, boxes):
            return self.GenSolvedGrid(rows)
        else:
            print "Soduko not solvable"
            sys.exit()

    #Backtracking search with constraints. 
    def solver(self, rows, columns, boxes):
        row, col = self.getEmptyCell(rows)
        if row == None and col == None:
            return True #Sudoku is filled-out completely and is solved
        for number in range(1, 10): #check all possible numbers that can be assigned
            if self.checkRCB(rows, columns, boxes, number, row, col):
                self.AssignNumber(rows, number, row, col) # Try assigning
                columns, boxes = self.updateRCB(rows) #update the Rows, Columns and Boxes
                if self.solver(rows, columns, boxes):
                    return True
                self.unAssignNumber(rows, number, row, col)
                columns, boxes = self.updateRCB(rows) #update the Rows, Columns and Boxes
        return False
                
    def getEmptyCell(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == "":
                    return row, col
        return None, None
                
    def unAssignNumber(self, grid, number, row, col):
        grid[row][col] = ""
        self.mistakes += 1
        
    def AssignNumber(self, grid, number, row, col):
        grid[row][col] = number
        self.assigned += 1

    #Constraints check. (A check whether a number is already in that row, column, or box) 
    def checkRCB(self, rows, columns, boxes, number, row, col):
        '''
        Return True if no conflicts found
        '''
        return number not in columns[col] and \
                number not in rows[row] and \
                self.checkBox(boxes, number, row, col)
    
    def checkBox(self, boxes, number, row, col):
        if row <= 2 and col <= 2:
            return number not in boxes[0]
        elif row <= 2 and 3 <= col <= 5:
            return number not in boxes[3]
        elif row <= 2 and 6 <= col <= 8:
            return number not in boxes[6]
        elif 3 <= row <= 5 and col <= 2:
            return number not in boxes[1]
        elif 3 <= row <= 5 and 3 <= col <= 5:
            return number not in boxes[4]
        elif 3 <= row <= 5 and 6 <= col <= 8:
            return number not in boxes[7]
        elif 6 <= row <= 8 and col <= 2:
            return number not in boxes[2]
        elif 6 <= row <= 8 and 3 <= col <= 5:
            return number not in boxes[5]
        elif 6 <= row <= 8 and 6 <= col <= 8:
            return number not in boxes[8]   
    
    def getRows(self, board):
        rows = []
        for i in range(0, 73, 9):
            row = board[i:i+9]
            rows.append(row)
        return rows
            
    def getColumns(self, board):
        columns = []
        for i in range(0,9):
            columns.append([x[i] for x in board])
        return columns
        
    def getBoxes(self, boardByRows):
        boxes = []
        for j in range(0, 9, 3):
            TopLevelBoxes = []
            MiddleLevelBoxes = []
            BottomLevelBoxes = []
            for i in range(0, 3):
                TopLevelBoxes = TopLevelBoxes + boardByRows[i][j:j+3]
                MiddleLevelBoxes = MiddleLevelBoxes + boardByRows[i+3][j:j+3]
                BottomLevelBoxes = BottomLevelBoxes + boardByRows[i+6][j:j+3]
            boxes.append(TopLevelBoxes)
            boxes.append(MiddleLevelBoxes)
            boxes.append(BottomLevelBoxes)
        return boxes
    
    def updateRCB(self, rows):
        columns = self.getColumns(rows)
        boxes   = self.getBoxes(rows)
        return columns, boxes
        
    def GenSolvedGrid(self, grid):
        return [item for sublist in grid for item in sublist]
    
                
