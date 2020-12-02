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
        self.subsquare_size = int(math.sqrt(size))
        self.subrow = [0 for i in range(self.subsquare_size)]
        self.subsquare = [self.subrow[:] for i in range(self.subsquare_size)]
        self.square = {i: self.subsquare[:] for i in range(0, self.size)}

    def __str__(self):
        strinG = ''
        for i in range(1, self.size + 1):
            strng_row = []
            for j in self.getRow(i):
                strng_row.append(str(j))
            row_strinG = ' '.join(strng_row)
            strinG += row_strinG + '\n'
        return strinG

    def populate_random_square(self):
        """
        Fills the sudoku board with randomly chosen characters from the appropriate symbol set.
        """
        for i in list(self.square.keys()):
            for j in range(self.subsquare_size):
                self.square[i][j] = [random.choice(self.chars) for i in range(self.subsquare_size)]

    def getCell(self, x, y):
        """
        Returns the character in a cell, determined by x == row number and y == column number.
        The code turns the input into the correct indices in order to access the cell.
        """
        subsquare_index = (((x - 1) // self.subsquare_size) * self.subsquare_size) + ((y - 1) // self.subsquare_size)
        subsquare_column_index = (y - 1) % self.subsquare_size
        subsquare_row_index = (x - 1) % self.subsquare_size
        return self.square[subsquare_index][subsquare_column_index][subsquare_row_index]

    def change_cell_random(self, x, y):
        """
        Inserts a random character into a chosen cell.
        The code turns the input into the correct indices in order to access the cell.
        """
        char = random.choice(self.chars)
        subsquare_index = (((x - 1) // self.subsquare_size) * self.subsquare_size) + ((y - 1) // self.subsquare_size)
        subsquare_column_index = (y - 1) % self.subsquare_size
        subsquare_row_index = (x - 1) % self.subsquare_size
        new_column = self.square[subsquare_index][subsquare_column_index][:]
        new_column[subsquare_row_index] = char
        self.square[subsquare_index][subsquare_column_index] = new_column

    def change_cell_to(self, x, y, char):
        """
        Changes character in a cell, determined by x == row number and y == column number.
        The code turns the input into the correct indices in order to access the cell.
        If using letters, use quotes around char. To delete, use 0.
        """
        subsquare_index = (((x - 1) // self.subsquare_size) * self.subsquare_size) + ((y - 1) // self.subsquare_size)
        subsquare_column_index = (y - 1) % self.subsquare_size
        subsquare_row_index = (x - 1) % self.subsquare_size
        new_column = self.square[subsquare_index][subsquare_column_index][:]
        new_column[subsquare_row_index] = char
        self.square[subsquare_index][subsquare_column_index] = new_column

    def user_change_cell(self):
        """
        Allows the player to change the character in a cell, given as a (row, column) coordinate.
        The code turns the input into the correct indices in order to access the cell.
        """
        cell = ast.literal_eval(input('Enter a cell to change in the form x,y where x is the row number and y is the column number: '))
        char = input('Enter character or 0 to delete: ')
        subsquare_index = (((int(cell[0]) - 1) // self.subsquare_size) * (self.subsquare_size)) + ((int(cell[1]) - 1) // self.subsquare_size)
        subsquare_column_index = (int(cell[1]) - 1) % self.subsquare_size
        subsquare_row_index = (int(cell[0]) - 1) % self.subsquare_size
        new_column = self.square[subsquare_index][subsquare_column_index][:]
        new_column[subsquare_row_index] = char
        self.square[subsquare_index][subsquare_column_index] = new_column

    def delete_cell(self, x, y):
        """
        Takes two integers (x == row number, y == column number) specifying a cell.
        Deletes the character in that cell (i.e. replaces it with a zero).
        """
        char = 0
        subsquare_index = (((x - 1) // self.subsquare_size) * self.subsquare_size) + ((y - 1) // self.subsquare_size)
        subsquare_column_index = (y - 1) % self.subsquare_size
        subsquare_row_index = (x - 1) % self.subsquare_size
        new_column = self.square[subsquare_index][subsquare_column_index][:]
        new_column[subsquare_row_index] = char
        self.square[subsquare_index][subsquare_column_index] = new_column

    def getRow(self, row):
        """
        Takes an integer in range(1, self.size + 1) indicating the row.
        Returns the row as a list.
        """
        subsquares_needed = [i for i in range(((row - 1) // self.subsquare_size) * self.subsquare_size, (((row - 1) // self.subsquare_size) + 1) * self.subsquare_size)]
        row_list = [self.square[i][j][(row - 1) % self.subsquare_size] for i in subsquares_needed for j in range(0, self.subsquare_size)]
        return row_list

    def isRowValid(self, row):
        """
        Takes an integer in range(1, self.size + 1) indicating the row.
        Returns True if there are no repeated characters (excluding 0).
        """
        row_list = self.getRow(row)
        row_chars = [i for i in row_list if i != 0]
        return all(row_chars.count(i) == 1 for i in row_chars)

    def getColumn(self, column):
        """
        Takes an integer in range(1, self.size + 1) indicating the column.
        Returns the column as a list.
        """
        subsquares_needed = [i for i in range((column - 1) // self.subsquare_size, self.size, self.subsquare_size)]
        column_list = [self.square[i][(column - 1) % self.subsquare_size][j] for i in subsquares_needed for j in range(0, self.subsquare_size)]
        return column_list

    def isColumnValid(self, column):
        """
        Takes an integer in range(1, self.size + 1) indicating the column.
        Returns True if there are no repeated characters (excluding 0).
        """
        column_list = self.getColumn(column)
        column_chars = [i for i in column_list if i != 0]
        return all(column_chars.count(i) == 1 for i in column_chars)

    def getSubsquare(self, x, y):
        """
        Takes two integers (x = row number, y = column number) specifying a cell.
        Returns the subsquare containing the cell, as a list of lists.
        """
        return self.square[(((x - 1) // self.subsquare_size) * self.subsquare_size) + ((y - 1) // self.subsquare_size)]

    def isSubsquareValid(self, x, y):
        """
        Takes two integers (x = row number, y = column number) specifying a cell.
        Returns True if there are no repeated entries (excluding 0) across all sublists in the subsquare containing the cell.
        """
        lst = list(itertools.chain(*self.getSubsquare(x, y)))
        return all(lst.count(char) == 1 for char in lst if char != 0)

    def isGridValid(self):
        """
        Returns True if all the rows, columns and subsquares are valid, False otherwise.
        """
        flag = True
        for i in range(1, self.size + 1):
            if not self.isRowValid(i) or not self.isColumnValid(i):
                flag = False
        for i, j in itertools.product(range(1, self.size + 1), range(1, self.size + 1)):
            if not self.isSubsquareValid(i, j):
                flag = False
        return flag

    def isCellValid(self, x, y):
        """
        Returns True if the entry in cell x, y is not repeated anywhere else in the same column, row or subsquare. False otherwise.
        """
        flag = True
        if self.getCell(x, y) != 0:
            if self.getRow(x).count(self.getCell(x, y)) > 1 or self.getColumn(y).count(self.getCell(x, y)) > 1 or list(itertools.chain(*self.getSubsquare(x, y))).count(self.getCell(x, y)) > 1:
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


def solveSudoku(grid):
    """
    grid is an instance of the Grid class, either empty or partially filled. Function uses a DFS type algorithm to try and 
    find a valid Sudoku based on the given grid.
    Returns True if there is a complete valid sudoku grid possible, and updates the grid along the way. False otherwise.
    """
    for i, j in itertools.product(range(1, grid.size + 1), range(1, grid.size + 1)):
        if grid.getCell(i, j) == 0:
            used_list = grid.getRow(i) + grid.getColumn(j) + list(itertools.chain(*grid.getSubsquare(i, j)))
            available_chars = [char for char in grid.chars if char not in used_list]
            if len(available_chars) != 0:           # If no available chars: break, return False and previous changed cell will try its next available char.
                random.shuffle(available_chars)
                for char in available_chars:
                    grid.change_cell_to(i, j, char)
                    if grid.isGridFull() or solveSudoku(grid):     # Recursive call effectively moves to the next non-zero cell.
                        return True
                grid.change_cell_to(i, j, 0)        # Nothing worked: reset cell to zero and try next available char for previous non-zero cell.
            break 
    return False


def createSudoku(grid, num_clues):
    """
    grid is an instance of the Grid class, filled with characters. Removes a number randomly and then uses the solveSudoku function to check whether 
    there is a valid Sudoku with a different number in that cell. Repeat until there are num_clues clues in the board. Since at each removal step we only 
    proceed if removal of that cell doesn't allow a new solution, uniqueness is guaranteed in the final puzzle (i.e. the original grid is the only solution). 
    Returns the grid with only num_clues non-zero cells (i.e. clues).
    """
    while grid.countNonEmptyCells() > num_clues:
        non_empty = grid.listNonEmptyCells()
        random.shuffle(non_empty)
        for cell in non_empty:
            i, j = cell
            orig_char = grid.getCell(i, j)
            used_list = grid.getRow(i) + grid.getColumn(j) + list(itertools.chain(*grid.getSubsquare(i, j)))
            available_chars = [char for char in grid.chars if char not in used_list]
            random.shuffle(available_chars)
            grid.delete_cell(i, j)
            flag = False
            for char in available_chars:
                grid_copy = copy.deepcopy(grid)
                grid_copy.change_cell_to(i, j, char)
                if solveSudoku(grid_copy):                  # Checks if removing cell creates a new solution.
                    flag = True
                    break
            if flag:
                grid.change_cell_to(i, j, orig_char)       # If it does then keep this cell and try another.
            else:
                break
    return grid


def playNewSudoku(size, symbols, num_clues):
    """
    size: square number between 4 and 100 inclusive
    symbols: 'letters' or 'numbers'
    num_clues: integer (for size 9: between 17 and 81)
    """
    grid = Grid(size, symbols)
    solveSudoku(grid)
    return createSudoku(grid, num_clues)



# Works but the createSudoku function is too slow (for size 9 when num_clues is near 20 it takes ages....)


# print(playNewSudoku(9, 'numbers', 20))
