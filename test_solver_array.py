import solver_array


def test_getForcedGuessCount_uses_covered_cells_for_guesses():
  assert solver_array.getForcedGuessCount(2, 2, (0, 0), [(1, 1)]) == 2


def test_getForcedGuessCount_returns_zero_without_guessing():
  assert solver_array.getForcedGuessCount(3, 3, (2, 2), [(0, 0)]) == 0


def test_getForcedGuessCount_can_guess_outside_the_frontier(monkeypatch):
  original_open_cell = solver_array.openCell
  state = {"guess_pending": False, "guess_cell": None, "frontier": set()}

  def tracked_print(*args, **kwargs):
    if args and args[0] == "No new moves can be made, adding a forced guess...":
      state["guess_pending"] = True

  def tracked_open_cell(cell, cell_type_board, cell_status_board):
    if state["guess_pending"]:
      for open_cell in solver_array.getUnsolvedCells(cell_status_board):
        state["frontier"].update(
          solver_array.getBoardCoveredNeighborsSet(open_cell, cell_status_board)
        )
      state["guess_cell"] = cell
      state["guess_pending"] = False
    return original_open_cell(cell, cell_type_board, cell_status_board)

  monkeypatch.setattr(solver_array, "print", tracked_print, raising=False)
  monkeypatch.setattr(solver_array, "openCell", tracked_open_cell)

  assert solver_array.getForcedGuessCount(4, 4, (1, 0), [(0, 0), (0, 2)]) == 2
  assert state["guess_cell"] not in state["frontier"]
