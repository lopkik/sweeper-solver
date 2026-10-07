import numpy as np
import numpy.typing as npt
from constraint import ExactSumConstraint, Problem
from neighborUtils import getBoardCoveredNeighborsSet, getBoardNeighborFlagCount, getBoardNeighborMineCount, getNeighborCellSet

# Cell type is:
#   -1 for Mines
#    0 for Empty
#  1-8 for Number of Neighbor Mines
def getCellTypeBoard(height: int, width: int, mine_positions: list[tuple]) -> npt.NDArray[np.int_]:
  cell_type_board = np.zeros((height, width), dtype=int)
  for i in range(height):
    for j in range(width):
      if (i, j) in mine_positions:
        cell_type_board[i][j] = -1
      else:
        cell_type_board[i][j] = 0

  for i in range(height):
    for j in range(width):
      if (i, j) not in mine_positions:
        cell_type_board[i][j] = getBoardNeighborMineCount((i, j), cell_type_board)

  return cell_type_board

# Cell Status is:
#   -3 for Flagged
#   -2 for Covered
#    0 for Opened
def getStartingCellStatusBoard(height: int, width: int) -> npt.NDArray[np.int_]:
  cell_status_board = np.full((height, width), -2, dtype=int)
  return cell_status_board  

def getCellSum(cell: tuple[int, int], cell_type_board: npt.NDArray[np.int_], cell_status_board: npt.NDArray[np.int_]) -> int:
  cellValue = cell_type_board[cell] if cell_status_board[cell] == 0 else cell_status_board[cell]
  if cellValue >= 0:
    return cellValue - getBoardNeighborFlagCount(cell, cell_status_board)
  else:
    return cellValue

def getCellSumBoard(cell_type_board: npt.NDArray[np.int_], cell_status_board: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
  cell_sum_board = cell_type_board.copy()
  for i in range(cell_type_board.shape[0]):
    for j in range(cell_type_board.shape[1]):
      cell = (i, j)
      cell_sum_board[cell] = getCellSum(cell, cell_type_board, cell_status_board)
  return cell_sum_board

def openCell(cell: tuple[int, int], cell_type_board: npt.NDArray[np.int_], cell_status_board: npt.NDArray[np.int_]):
  cellsToOpen = [cell]
  height, width = cell_type_board.shape

  while cellsToOpen:
    current_cell = cellsToOpen.pop()
    cell_status_board[current_cell] = 0

    if cell_type_board[current_cell] == 0:
      for neighbor in getNeighborCellSet(height, width, current_cell):
        if cell_status_board[neighbor] == -2:
          cellsToOpen.append(neighbor)

def flagCell(cell: tuple[int, int], cell_status_board: npt.NDArray[np.int_]):
  cell_status_board[cell] = -3

# Unsolved cells are opened, safe cells that have at least one covered neighbor
def getUnsolvedCells(cell_status_board: npt.NDArray[np.int_]) -> set[tuple[int, int]]:
  unsolvedCells = set()
  height, width = cell_status_board.shape

  for i in range(height):
    for j in range(width):
      if cell_status_board[(i, j)] == 0:
        for neighbor in getNeighborCellSet(height, width, (i, j)):
          if cell_status_board[neighbor] == -2:
            unsolvedCells.add((i, j))
            break

  return unsolvedCells

def checkSolvability(mineCount, cellSumBoard) -> bool:
  print("Checking solvability...", f"Mine count: {mineCount}", f"Flag Count: {np.count_nonzero(cellSumBoard == -3)}", sep="\n")
  return np.count_nonzero(cellSumBoard == -3) == mineCount

def constraintSolver(unsolvedCells, remainingMineCount, cellStatusBoard, cellSumBoard) -> tuple[set[tuple], set[tuple]]:
  variables = set()
  problem = Problem()

  for cell in unsolvedCells:
    covered_neighbors = getBoardCoveredNeighborsSet(cell, cellStatusBoard)
    for neighbor in covered_neighbors:
      variables.add(neighbor)
    problem.addConstraint(ExactSumConstraint(cellSumBoard[cell]), list(covered_neighbors))

  problem.addVariables(list(variables), [0, 1])  # 0 for safe, 1 for mine
  solutions = problem.getSolutions()
  print(solutions)

  safe_cells = set()
  mines = set()
  for covered_cell in variables:
    if all(solution[covered_cell] == 0 for solution in solutions):
      safe_cells.add(covered_cell)
    elif all(solution[covered_cell] == 1 for solution in solutions):
      mines.add(covered_cell)

  if not safe_cells and not mines:
    validSolns = [soln for soln in solutions if sum(soln.values()) == remainingMineCount]
    if len(validSolns) == 1:
      for covered_cell in variables:
        if validSolns[0][covered_cell] == 0:
          safe_cells.add(covered_cell)
        elif validSolns[0][covered_cell] == 1:
          mines.add(covered_cell)

  print(f"Safe cells: {safe_cells}")
  print(f"Mines: {mines}")
  return safe_cells, mines

def isSolvable(height: int, width: int, start_cell: tuple, mine_positions: list[tuple]) -> bool:
  cellTypeBoard = getCellTypeBoard(height, width, mine_positions)
  cellStatusBoard = getStartingCellStatusBoard(height, width)
  cellSumBoard = getCellSumBoard(cellTypeBoard, cellStatusBoard)

  openCell(start_cell, cellTypeBoard, cellStatusBoard)
  # set of opened, safe cells that have at least covered neighbor
  unsolvedCells = getUnsolvedCells(cellStatusBoard)
  cellSumBoard = getCellSumBoard(cellTypeBoard, cellStatusBoard)
  flagCount = 0

  while True:
    safe_cells, mines = constraintSolver(unsolvedCells, len(mine_positions) - flagCount, cellStatusBoard, cellSumBoard)
    for safe_cell in safe_cells:
      openCell(safe_cell, cellTypeBoard, cellStatusBoard  )
    for mine in mines:
      flagCell(mine, cellStatusBoard)
      flagCount += 1

    newUnsolvedCells = getUnsolvedCells(cellStatusBoard)
    if newUnsolvedCells == unsolvedCells:
      break
    unsolvedCells = newUnsolvedCells
    cellSumBoard = getCellSumBoard(cellTypeBoard, cellStatusBoard)

  return checkSolvability(len(mine_positions), cellSumBoard)

def printCellBoard(height, width, cell_dict):
  for i in range(height):
    for j in range(width):
      print(str(cell_dict[(i, j)]).rjust(2), end=' ')
    print()

# print(getCellTypeDict(9, 9, [(1,1), (2,2), (3,3)]))
printCellBoard(9, 9, getCellTypeBoard(9, 9, [(1,1), (2,2), (3,3)]))

isSolvable(9, 9, (5,5), [(1,1), (2,2), (3,3)])