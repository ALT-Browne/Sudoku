import math
import random
import ast
import itertools


class Grid(object):
    """
    Each instance has an associated list representing a square Sudoku grid composed of subsquares and cells. The cells initially contain zeros representing blank spaces.
    """
    def __init__(self, size, symbols):
        """
        Initialize class variables.

        param size: int
        param symbols: str - either "numbers" or "letters"
        """
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
        Get character in cell position (x, y) == (row, column).

        param x: int
        param y: int

        Return: int (if self.symbols == "numbers") or str (if self.symbols == "letters")
        """
        return self.cell_list[(x - 1) * self.size + y - 1]

    def change_cell_to(self, x, y, char):
        """
        Change character in cell position (x, y) == (row, column). If using letters, use quotes around char. To delete, use 0.

        param x: int
        param y: int
        param char: int (if self.symbols == "numbers" or 0 for deletion) or str (if self.symbols == "letters")
        """
        self.cell_list[(x - 1) * self.size + y - 1] = char

    def user_change_cell(self):
        """
        User change character in cell position (x, y) == (row, column).
        """
        cell = ast.literal_eval(input('Enter a cell to change in the form x,y where x is the row number and y is the column number: '))
        char = input('Enter character or 0 to delete: ')
        self.cell_list[(cell[0] - 1) * self.size + cell[1] - 1] = char

    def delete_cell(self, x, y):
        """
        Delete character in cell position (x, y) == (row, column).

        param x: int
        param y: int
        """
        self.cell_list[(x - 1) * self.size + y - 1] = 0

    def getRow(self, row_num):
        """
        Get row number row_num.
        
        param row_num: int

        Return: list of ints and str
        """
        return self.cell_list[(row_num - 1) * self.size : row_num * self.size]

    def isRowValid(self, row_num):
        """
        Check if row row_num contains each character (excluding 0) at most once.
        
        param row_num: int

        Return: bool
        """
        row_list = self.getRow(row_num)
        return all(row_list.count(char) == 1 for char in row_list if char != 0)

    def getColumn(self, column_num):
        """
        Get column number column_num.
        
        param column_num: int

        Return: list of ints and str
        """
        return self.cell_list[column_num - 1 : (self.size - 1) * self.size + column_num : self.size]

    def isColumnValid(self, column_num):
        """
        Check if column column_num contains each character (excluding 0) at most once.
        
        param column_num: int

        Return: bool
        """
        column_list = self.getColumn(column_num)
        return all(column_list.count(char) == 1 for char in column_list if char != 0)

    def getSubsquare(self, x, y):
        """
        Get subsquare containing cell position (x, y) == (row, column).
        
        param x: int
        param y: int

        Return: list of ints and str
        """
        return [self.getCell(k + 1, l + 1) for k in range(((x - 1) // self.sqrt_size) * self.sqrt_size, ((x - 1) // self.sqrt_size) * self.sqrt_size + self.sqrt_size) for l in range(((y - 1) // self.sqrt_size) * self.sqrt_size, ((y - 1) // self.sqrt_size) * self.sqrt_size + self.sqrt_size)]

    def isSubsquareValid(self, x, y):
        """
        Check if subsquare containing cell position (x, y) == (row, column) contains each character (excluding 0) at most once.
        
        param x: int
        param y: int

        Return: bool
        """
        subsquare_list = self.getSubsquare(x, y)
        return all(subsquare_list.count(char) == 1 for char in subsquare_list if char != 0)

    def isGridValid(self):
        """
        Check if all the rows, columns and subsquares are valid.

        Return: bool
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
        Check if the char in cell position (x, y) == (row, column) is repeated anywhere else in the same column, row or subsquare.

        param x: int
        param y: int

        Return: bool
        """
        flag = True
        if self.getCell(x, y) != 0:
            if self.getRow(x).count(self.getCell(x, y)) > 1 or self.getColumn(y).count(self.getCell(x, y)) > 1 or self.getSubsquare(x, y).count(self.getCell(x, y)) > 1:
                flag = False
        return flag

    def isGridFull(self):
        """
        Check if there are any empty cells (i.e. zeros) in the grid.

        Return: bool
        """
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) == 0:
                return False
        return True

    def countNonEmptyCells(self):
        """
        Count the number of non-zero characters in the grid.

        Return: int
        """
        count = 0
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) != 0:
                count += 1
        return count

    def listNonEmptyCells(self):
        """
        Find all non-empty cells (i.e. cell positions of non-zero characters).

        Return: list of tuples of ints
        """
        lst = []
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) != 0:
                lst.append((i, j))
        return lst

    def solveSudoku(self):
        """
        Use a DFS type algorithm to try and find a complete, valid Sudoku grid based on the current state of self.cell_list, and update along the way.

        Return: bool
        """
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if self.getCell(i, j) == 0:
                used_list = self.getRow(i) + self.getColumn(j) + self.getSubsquare(i, j)
                available_chars = [char for char in self.chars if char not in used_list]
                if len(available_chars) != 0:           # If no available chars: break, return False and previous changed cell will try its next available char.
                    random.shuffle(available_chars)
                    for char in available_chars:
                        self.change_cell_to(i, j, char)
                        if self.isGridFull() or self.solveSudoku():     # Recursive call effectively moves to the next empty cell.
                            return True
                    self.change_cell_to(i, j, 0)        # Nothing worked: reset cell to zero and try next available char for previous empty cell.
                break 
        return False
