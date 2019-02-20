import random

class nQueens:

    def __init__(self, n):
        self.board = [None] * n
        self.emptyRows = [i for i in range(n)]
        random.shuffle(self.emptyRows)
        self.occRows = [0] * n
        self.occLeftDiag = [0] * (2 * n - 1)
        self.occRightDiag = [0] * (2 * n - 1)
        self.totalConflicts = 0
        self.max_iterations = n * 2
        self.num_restarts = 0
        self.initialize(n)
        self.solve(n)


    def initialize(self, n):
        for col in range(n):
            if col == 0:
                rowVal = random.randint(0, n - 1)
                self.board[col] = rowVal + 1
                self.updateConflicts(rowVal, col, n)
            else:
                x = self.colConflicts(col, n)
                self.totalConflicts += x

    def colConflicts(self, col, n):
        oneConflict = []
        twoConflict = []
        for row in self.emptyRows:
            numConflicts = self.calcConflicts(row, col, n)

            if numConflicts == 0:
                self.board[col] = row + 1
                self.updateConflicts(row, col, n)
                return 0

            if numConflicts == 1:
                oneConflict.append(row)

            if numConflicts == 2:
                twoConflict.append(row)

        if len(oneConflict) == 0:
            rowVal = random.choice(twoConflict)
            self.board[col] = rowVal + 1
            self.updateConflicts(rowVal, col, n)
            return 2

        rowVal = random.choice(oneConflict)
        self.board[col] = rowVal + 1
        self.updateConflicts(rowVal, col, n)
        return 1

    def calcConflicts(self, row, col, n):
        if (row - col) >= 0:
            leftDiag = row - col
        else:
            leftDiag = (row - col) + (2*n - 1)        #Avoids negative values that would give the incorrect index
        rightDiag = row + col
        numConflicts = self.occRows[row] + self.occLeftDiag[leftDiag] + self.occRightDiag[rightDiag]
        return numConflicts

    def updateConflicts(self, row, col, n):
        if (row - col) >= 0:
            leftDiag = row - col
        else:
            leftDiag = (row - col) + (2*n - 1)   #Avoids negative values that would give the incorrect index
        self.occLeftDiag[leftDiag] += 1
        self.occRows[row] += 1
        self.occRightDiag[row + col] += 1
        self.emptyRows.remove(row)

    def solve(self, n):
        for i in range(self.max_iterations):
            if self.totalConflicts == 0:
                print("solution")
                return
            else:
                #Generates random column with at least 1 conflict
                randCol = random.randint(0, n - 1)
                oldRow = self.board[randCol]
                oldRow -= 1
                numConflicts = self.calcConflicts(oldRow, randCol, n) - 3
                while numConflicts < 1:
                    randCol = random.randint(0, n - 1)
                    oldRow = self.board[randCol]
                    oldRow -= 1
                    numConflicts = self.calcConflicts(oldRow, randCol, n) - 3

                noConflictUpdate = False
                for newRow in self.emptyRows:
                    numConflicts = self.calcConflicts(newRow, randCol, n)
                    if numConflicts == 0:
                        self.board[randCol] = newRow + 1
                        self.totalConflicts -= (self.calcConflicts(oldRow, randCol, n) - 3)
                        self.updateConflicts(newRow, randCol, n)
                        self.removeQueen(oldRow, randCol, n)
                        noConflictUpdate = True
                        break

                if noConflictUpdate == False:
                    twoConflicts = []
                    randRow = random.randint(0, n - 1)
                    numConflicts = self.calcConflicts(randRow, randCol, n)
                    counter = 0
                    #NEW
                    while numConflicts != 1:
                        randRow = random.randint(0, n - 1)
                        numConflicts = self.calcConflicts(randRow, randCol, n)
                        if numConflicts == 2:
                            twoConflicts.append(randRow)
                        counter += 1
                        if counter == int(n/3):
                            break

                    if numConflicts == 1:
                        self.board[randCol] = randRow + 1
                        self.totalConflicts -= ((self.calcConflicts(oldRow, randCol, n) - 3) - numConflicts)
                        self.updateSolveConflicts(randRow, randCol, n)
                        self.removeQueen(oldRow, randCol, n)
                    else:
                        if len(twoConflicts) > 0:
                            randRow = random.choice(twoConflicts)
                            self.board[randCol] = randRow + 1
                            self.totalConflicts -= ((self.calcConflicts(oldRow, randCol, n) - 3) - numConflicts)
                            self.updateSolveConflicts(randRow, randCol, n)
                            self.removeQueen(oldRow, randCol, n)
                        else:
                            while numConflicts > (self.calcConflicts(oldRow, randCol, n) - 3):
                                randRow = random.randint(0, n - 1)
                                numConflicts = self.calcConflicts(randRow, randCol, n)
                            self.board[randCol] = randRow + 1
                            self.totalConflicts -= ((self.calcConflicts(oldRow, randCol, n) - 3) - numConflicts)
                            self.updateSolveConflicts(randRow, randCol, n)
                            self.removeQueen(oldRow, randCol, n)

        self.num_restarts += 1
        print("restarting")
        self.restart(n)

    def removeQueen(self, oldRow, col, n):
        if (oldRow - col) >= 0:
            leftDiag = oldRow - col
        else:
            leftDiag = (oldRow - col) + (2*n - 1)   #Avoids negative values that would give the incorrect index
        self.occLeftDiag[leftDiag] -= 1
        self.occRows[oldRow] -= 1
        self.occRightDiag[oldRow + col] -= 1

        if self.occRows[oldRow] == 0:
            self.emptyRows.append(oldRow)

    #This function is purely to avoid the emptyRows.remove() in the other updateConflicts method
    def updateSolveConflicts(self, newRow, col, n):
        if (newRow - col) >= 0:
            leftDiag = newRow - col
        else:
            leftDiag = (newRow - col) + (2*n - 1)   ##Avoids negative values that would give the incorrect index
        self.occRows[newRow] += 1
        self.occLeftDiag[leftDiag] += 1
        self.occRightDiag[newRow + col] += 1

    def restart(self, n):
        self.board = [None] * n
        self.emptyRows = [i for i in range(n)]
        random.shuffle(self.emptyRows)
        self.occRows = [0] * n
        self.occLeftDiag = [0] * (2 * n - 1)
        self.occRightDiag = [0] * (2 * n - 1)
        self.totalConflicts = 0
        self.max_iterations = n*2
        self.initialize(n)
        self.solve(n)

def main():
    input = open("nqueens.txt")
    output = open("nqueens_out.txt", "w")
    lines = input.readlines()
    lines = [x.strip() for x in lines]
    lines = [int(i) for i in lines]
    for n in lines:
        initial_board = nQueens(n)
        #print(initial_board.board)
        #print(initial_board.totalConflicts)
        #print(initial_board.num_restarts)
        output.write(str(initial_board.board) + "\n")

main()
