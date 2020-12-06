from Sudoku import *
import sys

sys.setrecursionlimit(10**6)

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
            used_list = grid.getRow(i) + grid.getColumn(j) + grid.getSubsquare(i, j)
            available_chars = [char for char in grid.chars if char not in used_list]
            random.shuffle(available_chars)
            grid.delete_cell(i, j)
            flag = False
            for char in available_chars:      
                grid_copy = copy.deepcopy(grid)
                grid_copy.change_cell_to(i, j, char)
                if grid_copy.solveSudoku():                  # Checks if removing cell creates a new solution.
                    flag = True
                    break
            if flag:
                grid.change_cell_to(i, j, orig_char)       # If it does then keep this cell and try another.
            else:
                break
    return grid

# Works but the createSudoku function is too slow (for size 9 when num_clues is near 20 it takes ages....)
# Could be due to the deep copy function because i used nested lists?

def playNewSudoku(size, symbols, num_clues):
    """
    size: square number between 4 and 100 inclusive
    symbols: 'letters' or 'numbers'
    num_clues: integer (for size 9: between 17 and 81)
    """
    grid = Grid(size, symbols)
    grid.solveSudoku()
    return createSudoku(grid, num_clues)


if __name__ == "__main__":
    print(playNewSudoku(9, 'numbers', 25))