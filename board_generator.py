import numpy as np
import numpy.typing as npt

def generate_mine_positions(height: int, width: int, num_mines: int, start_cell: tuple[int, int]) -> list[tuple[int, int]]:
  all_cells = [
    (i, j)
    for i in range(height)
    for j in range(width)
    if max(abs(i - start_cell[0]), abs(j - start_cell[1])) > 1
  ]
  mine_positions = np.random.choice(len(all_cells), size=num_mines, replace=False)
  return [all_cells[i] for i in mine_positions]
