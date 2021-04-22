from Sudoku_class import *
import sys

sys.setrecursionlimit(10**6)

def createSudoku(grid, num_clues):
    """
    Find valid Sudoku puzzle from the cell_list associated to the given grid such that the original is the unique solution.

    Method: delete a cell randomly and then use the solveSudoku function to check whether 
    there is a valid Sudoku with a different number in that cell. Repeat until there are num_clues clues in the board. Since at each removal step we only 
    proceed if removal of that cell doesn't allow a new solution, uniqueness is guaranteed in the final puzzle (i.e. the original grid is the only solution).
    
    Note: there is no known lower bound (in general) which is sufficient for every Sudoku of a given size (although it must be at least 17 for size 9). Thus, the function may not return the desired number of clues.

    param grid: Grid instance (filled)
    param num_clues: int - (e.g. for size 9, must be between 17 and 81)
    
    Return: Grid instance (not filled)
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
