from Sudoku import *
import sys

sys.setrecursionlimit(10**6)

def createSudoku(grid, num_clues):
    """
    grid is an instance of the Grid class, filled with characters. Removes a number randomly and then uses the solveSudoku function to check whether 
    there is a valid Sudoku with a different number in that cell. Repeat until there are num_clues clues in the board. Since at each removal step we only 
    proceed if removal of that cell doesn't allow a new solution, uniqueness is guaranteed in the final puzzle (i.e. the original grid is the only solution).

    Returns the grid with only num_clues non-zero cells (i.e. clues).
    
    HOWEVER, there is no known lower bound (in general) which is sufficient for every Sudoku of a given size (although it must be at least 17 for size 9).
    The dead_ends stopping condition ensures the algorithm terminates in a reasonable time, but it means (especially for a low num_clues number)
    it may not return the desired number of clues.
    """
    dead_ends = 0
    while grid.countNonEmptyCells() > num_clues and dead_ends <= 10:    # Increase dead_ends bound to allow a longer search
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
                grid.change_cell_to(i, j, orig_char)
                dead_ends += 1       # If it does then keep this cell and try another.
            else:
                break
    return grid


# Optimise by keeping a record of which cells have reached a dead end rather than doing it randomly each time round the while loop
# This might help if it is true that: getting a dead end for a particular cell is not affected by the removal of another cell later.... 
# i.e i dont need to check a cell again later on if it has already produced a dead end in a previous looping


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
    print(playNewSudoku(9, 'numbers', 17))