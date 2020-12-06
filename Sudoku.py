import math
import random
import ast
import itertools
import copy


class Grid(object):
    """
    Each instance will be a square grid composed of subsquares and cells which initially contain zeros representing blank spaces.
    """
    def __init__(self, size, symbols):
        self.size = size
        self.symbols = symbols
        self.letters = 'abcdefghijklmnopqrstuvwxyz'
        self.numbers = [i for i in range(1, 101)]
        self.letters_choice = self.letters[0:self.size]
        self.numbers_choice = self.numbers[0:self.size]
        self.numlet_choice = {'letters': self.letters_choice, 'numbers': self.numbers_choice}
        self.chars = self.numlet_choice[self.symbols]
        self.sqrt_size = int(math.sqrt(size))
        self.cell_list = [0 for i in range(self.size ** 2)]

    def __str__(self):
        strinG = ''
        for i in range(1, self.size + 1):
            strng_row = []
            for j in self.getRow(i):
                strng_row.append(str(j))
            row_strinG = ' '.join(strng_row)
            strinG += row_strinG + '\n'
        return strinG

    def getCell(self, x, y):
        """
        Returns the character in a cell, determined by x == row number and y == column number.
        The code turns the input into the correct indices in order to access the cell.
        """
        return self.cell_list[(x - 1) * self.size + y - 1]

    def change_cell_to(self, x, y, char):
        """
        Changes character in a cell, determined by x == row number and y == column number.
        The code turns the input into the correct indices in order to access the cell.
        If using letters, use quotes around char. To delete, use 0.
        """
        self.cell_list[(x - 1) * self.size + y - 1] = char

    def user_change_cell(self):
        """
        Allows the player to change the character in a cell, given as a (row, column) coordinate.
        The code turns the input into the correct indices in order to access the cell.
        """
        cell = ast.literal_eval(input('Enter a cell to change in the form x,y where x is the row number and y is the column number: '))
        char = input('Enter character or 0 to delete: ')
        self.cell_list[(cell[0] - 1) * self.size + cell[1] - 1] = char

    def delete_cell(self, x, y):
        """
        Takes two integers (x == row number, y == column number) specifying a cell.
        Deletes the character in that cell (i.e. replaces it with a zero).
        """
        self.cell_list[(x - 1) * self.size + y - 1] = 0

    def getRow(self, row):
        """
        Takes an integer in range(1, self.size + 1) indicating the row.
        Returns the row as a list.
        """
        return self.cell_list[(row - 1) * self.size : row * self.size]

    def isRowValid(self, row):
        """
        Takes an integer in range(1, self.size + 1) indicating the row.
        Returns True if there are no repeated characters (excluding 0).
        """
        row_list = self.getRow(row)
        return all(row_list.count(char) == 1 for char in row_list if char != 0)

    def getColumn(self, column):
        """
        Takes an integer in range(1, self.size + 1) indicating the column.
        Returns the column as a list.
        """
        return self.cell_list[column - 1 : (self.size - 1) * self.size + column : self.size]

    def isColumnValid(self, column):
        """
        Takes an integer in range(1, self.size + 1) indicating the column.
        Returns True if there are no repeated characters (excluding 0).
        """
        column_list = self.getColumn(column)
        return all(column_list.count(char) == 1 for char in column_list if char != 0)

    def getSubsquare(self, x, y):
        """
        Takes two integers (x = row number, y = column number) specifying a cell.
        Returns the subsquare containing the cell, as a list.
        """
        return [self.getCell(k + 1, l + 1) for k in range(((x - 1) // self.sqrt_size) * self.sqrt_size, ((x - 1) // self.sqrt_size) * self.sqrt_size + self.sqrt_size) for l in range(((y - 1) // self.sqrt_size) * self.sqrt_size, ((y - 1) // self.sqrt_size) * self.sqrt_size + self.sqrt_size)]

    def isSubsquareValid(self, x, y):
        """
        Takes two integers (x = row number, y = column number) specifying a cell.
        Returns True if there are no repeated entries (excluding 0) across all sublists in the subsquare containing the cell.
        """
        subsquare_list = self.getSubsquare(x, y)
        return all(subsquare_list.count(char) == 1 for char in subsquare_list if char != 0)

    def isGridValid(self):
        """
        Returns True if all the rows, columns and subsquares are valid, False otherwise.
        """
        flag = True
        for i in range(1, self.size + 1):
            if not self.isRowValid(i) or not self.isColumnValid(i):
                flag = False
        for i, j in itertools.product(range(1, 1 + (self.sqrt_size - 1) * self.sqrt_size + 1, self.sqrt_size), range(1, 1 + (self.sqrt_size - 1) * self.sqrt_size + 1, self.sqrt_size)):
            if not self.isSubsquareValid(i, j):
                flag = False
        return flag

    def isCellValid(self, x, y):
        """
        Returns True if the entry in cell x, y is not repeated anywhere else in the same column, row or subsquare. False otherwise.
        """
        flag = True
        if self.getCell(x, y) != 0:
            if self.getRow(x).count(self.getCell(x, y)) > 1 or self.getColumn(y).count(self.getCell(x, y)) > 1 or self.getSubsquare.count(self.getCell(x, y)) > 1:
                flag = False
        return flag

    def isGridFull(self):
        """
        Checks to see if there are any gaps (i.e. zeros) in the grid.
        """
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) == 0:
                return False
        return True

    def countNonEmptyCells(self):
        """
        Counts the number of non-zeros in the grid.
        """
        count = 0
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) != 0:
                count += 1
        return count

    def listNonEmptyCells(self):
        """
        Returns a list of tuples (i, j) where i == row numebr and j = column number of a non-empty cell.
        """
        lst = []
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) != 0:
                lst.append((i, j))
        return lst

    def solveSudoku(self):
        """
        grid is an instance of the Grid class, either empty or partially filled. Function uses a DFS type algorithm to try and 
        find a valid Sudoku based on the given grid.
        Returns True if there is a complete valid sudoku grid possible, and updates the grid along the way. False otherwise.
        """
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) == 0:
                used_list = self.getRow(i) + self.getColumn(j) + self.getSubsquare(i, j)
                available_chars = [char for char in self.chars if char not in used_list]
                if len(available_chars) != 0:           # If no available chars: break, return False and previous changed cell will try its next available char.
                    random.shuffle(available_chars)
                    for char in available_chars:
                        self.change_cell_to(i, j, char)
                        if self.isGridFull() or self.solveSudoku():     # Recursive call effectively moves to the next non-zero cell.
                            return True
                    self.change_cell_to(i, j, 0)        # Nothing worked: reset cell to zero and try next available char for previous non-zero cell.
                break 
        return False
