from constraint import *

problem = Problem()

problem.addVariable('a', [1, 2, 3])
problem.addVariable('b', [4, 5, 6])

solutions = problem.getSolutions()
print(solutions)
print('test')

type MinesweeperInstance = tuple[int, int, tuple[int, int], list[tuple[int, int]]]

minesweeper_instance: MinesweeperInstance = (9, 9, (5, 5), [(1,1), (2,2), (3,3), (1,2), (2,1), (9,9), (8,8), (7,7)])

def isSolvable(m):
  unsolved = set()
  cellTypeBoard = []
  cellSumBoard = []

  
  pass