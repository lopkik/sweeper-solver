from constraint import *

problem = Problem()

problem.addVariable('a', [1, 2, 3])
problem.addVariable('b', [4, 5, 6])

solutions = problem.getSolutions()
print(solutions)
print('test')

type MinesweeperInstance = tuple[int, int, tuple[int, int], list[tuple[int, int]]]

minesweeper_instance: MinesweeperInstance = (9, 9, (5, 5), [(1,1), (2,2), (3,3), (1,2), (2,1), (9,9), (8,8), (7,7)])



def getNeighborMineCount(cell, cell_type_dict):
  count = 0
  i, j = cell
  for di in [-1, 0, 1]:
    for dj in [-1, 0, 1]:
      if di == 0 and dj == 0:
        continue
      neighbor = (i + di, j + dj)
      if neighbor in cell_type_dict and cell_type_dict[neighbor] == -1:
        count += 1
  return count

def getNeighborFlagCount(cell, cell_status_dict):
  count = 0
  i, j = cell
  for di in [-1, 0, 1]:
    for dj in [-1, 0, 1]:
      if di == 0 and dj == 0:
        continue
      neighbor = (i + di, j + dj)
      if neighbor in cell_status_dict and cell_status_dict[neighbor] == -3:
        count += 1
  return count

def getNeighborCellSet(height, width, cell):
  i, j = cell
  neighbor_set = set()
  for di in [-1, 0, 1]:
    for dj in [-1, 0, 1]:
      if di == 0 and dj == 0:
        continue
      neighbor = (i + di, j + dj)
      if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
        neighbor_set.add(neighbor)
  return neighbor_set

# Cell type is:
#   -1 for Mines
#    0 for Empty
#  1-8 for Number of Neighbor Mines
def getCellTypeDict(height, width, mine_positions):
  cell_type_dict = {}
  for i in range(height):
    for j in range(width):
      if (i, j) in mine_positions:
        cell_type_dict[(i, j)] = -1
      else:
        cell_type_dict[(i, j)] = 0

  for i in range(height):
    for j in range(width):
      if (i, j) not in mine_positions:
        cell_type_dict[(i, j)] = getNeighborMineCount((i, j), cell_type_dict)

  return cell_type_dict

# Cell Status is:
#   -3 for Flagged
#   -2 for Covered
#    0 for Opened
def getStartingCellStatusDict(height, width):
  cell_status_dict = {}
  for i in range(height) :
    for j in range(width):
      cell_status_dict[(i, j)] = -2

  return cell_status_dict

def getCellValue(cell, cell_type_dict, cell_status_dict):
  return cell_type_dict[cell] if cell_status_dict[cell] == 0 else cell_status_dict[cell]



def getCellSum(cell, cell_type_dict, cell_status_dict):
  cellValue = getCellValue(cell, cell_type_dict, cell_status_dict)
  if cellValue >= 0:
    return cellValue - getNeighborFlagCount(cell, cell_status_dict)
  else:
    return cellValue

def getCellSumDict(cell_type_dict, cell_status_dict):
  cell_sum_dict = {}
  for cell in cell_type_dict:
    cell_sum_dict[cell] = getCellSum(cell, cell_type_dict, cell_status_dict)
  return cell_sum_dict

def openCell(cell, height, width, cell_type_dict, cell_status_dict):
  cellsToOpen = [cell]

  while cellsToOpen:
    current_cell = cellsToOpen.pop()
    cell_status_dict[current_cell] = 0

    if cell_type_dict[current_cell] == 0:
      for neighbor in getNeighborCellSet(height, width, current_cell):
        if cell_status_dict[neighbor] == -2:
          cellsToOpen.append(neighbor)

def flagCell(cell, cell_status_dict):
  cell_status_dict[cell] = -3

# Unsolved cells are opened, safe cells that have at least one covered neighbor
def getUnsolvedCells(height, width, cellStatusDict):
  unsolvedCells = set()

  for i in range(height):
    for j in range(width):
      if cellStatusDict[(i, j)] == 0:
        for neighbor in getNeighborCellSet(height, width, (i, j)):
          if cellStatusDict[neighbor] == -2:
            unsolvedCells.add((i, j))
            break

  return unsolvedCells

def checkSolvability(cellSumDict) -> bool:
  pass

def constraintSolver(unsolvedCells, cellSumDict) -> tuple[set[tuple], set[tuple]]:
  pass

def isSolvable(height: int, width: int, start_cell: tuple, mine_positions: list[tuple]) -> bool:
  # set of opened, safe cells that have at least covered neighbor
  unsolvedCells = set()
  cellTypeDict = getCellTypeDict(height, width, mine_positions)
  cellStatusDict = getStartingCellStatusDict(height, width)
  cellSumDict = getCellSumDict(cellTypeDict, cellStatusDict)

  openCell(start_cell, height, width, cellTypeDict, cellStatusDict)
  unsolvedCells = getUnsolvedCells(height, width, cellStatusDict)

  while True:
    safe_cells, mines = constraintSolver(unsolvedCells, cellSumDict)
    for safe_cell in safe_cells:
      openCell(safe_cell, height, width, cellTypeDict, cellStatusDict)
    for mine in mines:
      flagCell(mine, cellStatusDict)
    break

  return checkSolvability(cellSumDict)

def printCellBoard(height, width, cell_dict):
  for i in range(height):
    for j in range(width):
      print(str(cell_dict[(i, j)]).rjust(2), end=' ')
    print()

# print(getCellTypeDict(9, 9, [(1,1), (2,2), (3,3)]))
printCellBoard(9, 9, getCellTypeDict(9, 9, [(1,1), (2,2), (3,3)]))