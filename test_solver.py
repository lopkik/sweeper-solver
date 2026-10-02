import copy
from solver import openCell, getStartingCellStatusDict, getCellTypeDict

def test_openCell_simple():
  cell = (2, 2)
  height = 3
  width = 3
  minePositions = [(0, 0)]
  cellTypeDict = getCellTypeDict(height, width, minePositions)
  originalCellTypeDict = copy.deepcopy(cellTypeDict)
  cellStatusDict = getStartingCellStatusDict(height, width)
  originalCellStatusDict = copy.deepcopy(cellStatusDict)

  openCell(cell, height, width, cellTypeDict, cellStatusDict)

  assert cellTypeDict == originalCellTypeDict
  assert cellStatusDict != originalCellStatusDict
  assert cellStatusDict == {
    (0,0): -2, (0,1): 0, (0,2): 0, 
    (1,0): 0, (1,1): 0, (1,2): 0, 
    (2,0): 0, (2,1): 0, (2,2): 0
    }

def test_openCell_complex():
  cell = (2, 2)
  height = 5
  width = 5
  minePositions = [(0, 0), (0, 2), (0, 4), (2, 0), (2, 4), (4, 0), (4, 2), (4, 4)]
  cellTypeDict = getCellTypeDict(height, width, minePositions)
  originalCellTypeDict = copy.deepcopy(cellTypeDict)
  cellStatusDict = getStartingCellStatusDict(height, width)
  originalCellStatusDict = copy.deepcopy(cellStatusDict)

  openCell(cell, height, width, cellTypeDict, cellStatusDict)

  assert cellTypeDict == originalCellTypeDict
  assert cellStatusDict != originalCellStatusDict
  assert cellStatusDict == {
    (0,0): -2, (0,1): -2, (0,2): -2, (0,3): -2, (0,4): -2,
    (1,0): -2, (1,1): 0, (1,2): 0, (1,3): 0, (1,4): -2,
    (2,0): -2, (2,1): 0, (2,2): 0, (2,3): 0, (2,4): -2,
    (3,0): -2, (3,1): 0, (3,2): 0, (3,3): 0, (3,4): -2,
    (4,0): -2, (4,1): -2, (4,2): -2, (4,3): -2, (4,4): -2
    }