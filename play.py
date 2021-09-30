from create_Sudoku import *

def playNewSudoku(size, symbols, num_clues):
    """
    Find a valid Sudoku puzzle with num_clues clues.
    
    param size: int - square number between 4 and 100 inclusive
    param symbols: str - either "numbers" or "letters"
    param num_clues: int - (e.g. for size 9, must be between 17 and 81)

    Return: Grid instance - not necessarily with the desired number of clues
    """
    grid = Grid(size, symbols)
    grid.solveSudoku()
    return createSudoku(grid, num_clues)
    

if __name__ == "__main__":
    print(playNewSudoku(9, 'numbers', 35))