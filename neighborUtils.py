import numpy as np
import numpy.typing as npt

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

def getBoardNeighborMineCount(cell, cell_type_board: npt.NDArray[np.int_]) -> int:
  i, j = cell
  height, width = cell_type_board.shape
  segment = cell_type_board[max(0, i-1):min(height, i+2), max(0, j-1):min(width, j+2)]
  count = np.count_nonzero(segment == -1)
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

def getBoardNeighborFlagCount(cell, cell_status_board: npt.NDArray[np.int_]) -> int:
  i, j = cell
  height, width = cell_status_board.shape
  segment = cell_status_board[max(0, i-1):min(height, i+2), max(0, j-1):min(width, j+2)]
  count = np.count_nonzero(segment == -3)
  return count

def getNeighborCellSet(height: int, width: int, cell: tuple[int, int]) -> set[tuple[int, int]]:
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

def getCoveredNeighborsSet(height, width, cell, cell_status_dict):
  i, j = cell
  covered_neighbors = set()
  for di in [-1, 0, 1]:
    for dj in [-1, 0, 1]:
      if di == 0 and dj == 0:
        continue
      neighbor = (i + di, j + dj)
      if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
        if cell_status_dict[neighbor] == -2:
          covered_neighbors.add(neighbor)
  return covered_neighbors

def getBoardCoveredNeighborsSet(cell: tuple[int, int], cell_status_board: npt.NDArray[np.int_]) -> set[tuple[int, int]]:
  i, j = cell
  covered_neighbors = set()
  height, width = cell_status_board.shape

  for di in [-1, 0, 1]:
    for dj in [-1, 0, 1]:
      if di == 0 and dj == 0:
        continue
      neighbor = (i + di, j + dj)
      if 0 <= neighbor[0] < height and 0 <= neighbor[1] < width:
        if cell_status_board[neighbor] == -2:
          covered_neighbors.add(neighbor)
  return covered_neighbors