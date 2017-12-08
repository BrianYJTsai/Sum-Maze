#  File: sumMaze.py
#  Description: This program checks whether you can find a way out of a maze by searching for a path that adds up to the
#  target value. A random numbered maze is generated and the program shows the steps to find the solution.
#  Student's Name: Brian Tsai
#  Student's UT EID: byt76
#  Course Name: CS 313E
#  Unique Number: 51465
#
#  Date Created: 11/11/17
#  Date Last Modified: 11/11/17

class State():

    # Create a new state
    def __init__(self, grid, history, start_row, start_col, sum):
        self.grid = grid
        self.history = history
        self.start_row = start_row
        self.start_col = start_col
        self.sum = sum

    # Get the state's current row
    def getStartRow(self):
        return self.start_row

    # Get the state's current column
    def getStartCol(self):
        return self.start_col

    # Get this state's grid
    def getGrid(self):
        return self.grid

    # Get this state's path history
    def getHistory(self):
        return self.history

    # Get the state's current sum
    def getSum(self):
        return self.sum

    # Add the current location's value to the sum
    def addToSum(self):
        self.sum += int(self.grid[self.start_row][self.start_col])

    # Drop a breadcrumb on the current location
    def dropBreadCrumb(self):
        self.grid[self.start_row][self.start_col] = "X"

    # Add the current location to the path history
    def addToHistory(self):
        self.history.append(self.grid[self.start_row][self.start_col])

    # Return a string representation of this state state
    def __str__(self):
        grid = [['{:<4}'.format(number) for number in row] for row in self.grid]
        grid = [' '.join(row) for row in grid]
        grid = [("      " + row) for row in grid]
        grid = ('\n'.join(grid)) + "\n"
        grid = "   Grid:\n" + grid
        history = "   history: " + str(self.history) + "\n"
        start = "   start point: " + "(" + str(self.start_row) + "," + str(self.start_col) + ")" + "\n"
        sum = "   sum so far: " + str(self.sum) + "\n"
        return grid + history + start + sum



# Constants to define the relative directions
directions = ["right", "up", "down", "left"]
directionValue = {"right" : [0, 1], "up" : [-1, 0], "down": [1, 0], "left": [0, -1]}

def solve(state, width, height, targetSum, end_row, end_col):


    # Drop a breadcrumb and add the value of this location to the path history
    state.addToSum()
    state.addToHistory()
    state.dropBreadCrumb()
    print(state)

    print("Is this a goal state?")

    # Check whether this is the end of the maze
    if (state.getStartRow() == end_row and state.getStartCol() == end_col):
        if (state.getSum() == targetSum):
            print("Solution found!")
            print(state.getHistory())
            return state.getHistory()
        else:
            return None


    # Check whether the sum has exceeded the target sum
    if (state.getSum() > targetSum):
        print("No.", end = " ")
        print("Target exceeded:  abandoning path")
        return None


    start_row = state.getStartRow()
    start_col = state.getStartCol()
    sum = state.getSum()

    # Test all four directions recursively for a possible path
    for direction in directions:
        row = start_row + directionValue[direction][0]
        col = start_col + directionValue[direction][1]
        grid = state.getGrid()
        grid = [row[:] for row in grid]
        print("No. ", end = " ")
        print("Can I move", str(direction) + "?")

        # Check whether each direction has a valid path
        if (isValid(grid, width, height, row, col)):
            print("Yes!")
            print("Paused...\n")
            history = state.getHistory().copy()
            directionState = State(grid, history, row, col, sum)
            print("Problem is now:")
            result = solve(directionState, width, height, targetSum, end_row, end_col)
            if (result != None):
                return result

    # Return if there are no possible directions to move in
    print("Couldn't move in any direction.  Backtracking.")
    return None



# Check whether the row and col are valid to move unto
def isValid(grid, width, height, row, col):
    return (row >= 0 and row < height and col >= 0 and col < width and grid[row][col] != "X")

def main():
    input = open("mazedata3.txt", "r")

    # Get all of the maze's metadata
    line = input.readline()
    line = line.strip()
    line = line.split()
    targetSum = int(line[0])
    height = int(line[1])
    width = int(line[2])
    start_row = int(line[3])
    start_col = int(line[4])
    end_row = int(line[5])
    end_col = int(line[6])

    matrix = []

    # Create a matrix from the input file
    for line in input:
        line = line.strip()
        line = line.split()
        line = [int(number) for number in line]
        matrix.append(line)

    # Create the initial state
    state = State(matrix, [], start_row, start_col, 0)

    # Output the solution to the maze
    solve(state, width, height, targetSum, end_row, end_col)

    input.close()

main()