from Sudoku import *
import sys

sys.setrecursionlimit(10**6)

def createSudoku(grid, num_clues):
    """
    grid is an instance of the Grid class, filled (at least partially) with characters. Removes a number randomly and then uses the solveSudoku function to check whether 
    there is a valid Sudoku with a different number in that cell. Repeat until there are num_clues clues in the board. Since at each removal step we only 
    proceed if removal of that cell doesn't allow a new solution, uniqueness is guaranteed in the final puzzle (i.e. the original grid is the only solution).

    Returns the grid with only num_clues non-zero cells (i.e. clues).
    
    HOWEVER, there is no known lower bound (in general) which is sufficient for every Sudoku of a given size (although it must be at least 17 for size 9). Thus, it may not return the desired number of clues.
    """
    non_empty = grid.listNonEmptyCells()
    random.shuffle(non_empty)
    
    for cell in non_empty:
        if grid.countNonEmptyCells() > num_clues:
            i, j = cell
            orig_char = grid.getCell(i, j)
            used_list = grid.getRow(i) + grid.getColumn(j) + grid.getSubsquare(i, j)
            available_chars = [char for char in grid.chars if char not in used_list]
            random.shuffle(available_chars)
            grid.delete_cell(i, j)
            flag = False
            grid_copy = Grid(grid.size, grid.symbols)
            grid_copy.cell_list = grid.cell_list[:]
            for char in available_chars:            # Checks if removing cell creates a new solution.
                grid_copy.change_cell_to(i, j, char)
                if grid_copy.solveSudoku():
                    flag = True
                    break
            if flag:                            # If it does then keep this cell and try the next one.
                grid.change_cell_to(i, j, orig_char)
    return grid

# Possible optimisation in solution (rather than time):
# at each stage where i remove a cell, check to see how many other cells it turns in to dead ends. The more cells it turns in to dead ends the fewer cells i will be able to remove overall? Thus it could be a good idea to chek every nonempty cell (that is not already known to be a dead end) at each step, and remove the one who creates the fewest dead ends..... This could be a good way to get the most possible cells removed and therefore get to higher difficulty level. This will not affect those cells that were already dead ends before the current cells is (potentially) removed.


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
    print(playNewSudoku(9, 'numbers', 20))