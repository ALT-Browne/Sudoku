# This is a Sudoku creater

## It uses a DFS type algorithm to create a valid puzzle with a given number of clues (or close to it!)

## Next steps

- Speed up algorithm by making the solveSudoku function faster. Instead of trying random cells, find a better method. This is important because, for a low number of clues, the createSudoku function runs too slow at the moment.

- Another possible optimisation (in solution, not speed) is in the createSudoku function. At the moment it does not always achieve the desired number of clues for low numbers (numbers approaching 17, in the 9x9 case). Firstly, this could happen because the solved grid it makes before removing numbers may not be solvable from the desired number. Secondly, this could happen because there is a smarter way of removing cells than just choosing the first random one which still keeps the solution unique. This is because, despite the fact that a given cell's removal might not destroy uniqueness, it could make other cells into "dead-ends", i.e. their subsequent removal would destroy uniqueness. Thus, at each step, it seems prudent to remove a cell which both keeps uniqueness right away, and creates the fewest new dead-ends as possible. This may allow more clues to be removed than the current method. Note that once a cell is known to be a dead-end then it will be one forever. Thus if we keep a list of dead-ends then at each step we would only need to check the remaining cells for dead-endedness.

- Change the num_clues parameter to a difficulty parameter. This would avoid the problem of a grid not being solvable for a low number of clues.

- Create a GUI.
