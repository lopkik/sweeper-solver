from collections import Counter
import math
import numpy as np
import statistics
import time
from board_generator import generate_mine_positions
from solver_array import getForcedGuessCount, printCellConfig

def run_board(height: int, width: int, mine_count: int, runs: int):
  print(f"Running {height}x{width} board with {mine_count} mines for {runs} runs...")
  total_forced_guesses = 0
  forced_guess_counts = Counter()
  min_guesses = float('inf')
  max_guesses = float('-inf')

  for i in range(runs):
    start_cell = (np.random.randint(0, height), np.random.randint(0, width))
    mines = generate_mine_positions(height, width, mine_count, start_cell)
    forced_guess_count = getForcedGuessCount(height, width, start_cell, mines)

    total_forced_guesses += forced_guess_count
    forced_guess_counts[forced_guess_count] += 1
    min_guesses = min(min_guesses, forced_guess_count)
    max_guesses = max(max_guesses, forced_guess_count)

    if (i + 1) % 500 == 0:
      print(f"Completed {i + 1} runs...")

  print("AVG FG, AVG FG sans NG runs, FG std dev, Min FG, Max FG")
  print(f"{total_forced_guesses / runs:.4f}, {total_forced_guesses / (runs - forced_guess_counts[0]):.4f}, {statistics.stdev(forced_guess_counts.elements()):.4f}, {min_guesses}, {max_guesses}")
  # print(f"Avg forced guess count for {height}x{width} board with {mine_count} mines: {total_forced_guesses / runs}")
  # print(f"Avg forced guess count sans no guess runs: {total_forced_guesses / (runs - forced_guess_counts[0])}")
  # print(f"Forced guess count std dev: {statistics.stdev(forced_guess_counts.elements()):.4f}")
  # print(f"Forced guess count distribution: {sorted(dict(forced_guess_counts).items())}")
  # print(f"Min forced guesses: {min_guesses}")
  # print(f"Max forced guesses: {max_guesses}")


# Beginner boards (9x9 with 10 mines)
# start = time.perf_counter()
# run_board(9, 9, 10, 5000)
# end = time.perf_counter()
# print(f"Time elapsed for beginner boards: {end - start:.4f} seconds")

# Intermediate boards (16x16 with 40 mines)
# start = time.perf_counter()
# run_board(16, 16, 40, 5000)
# end = time.perf_counter()
# print(f"Time elapsed for intermediate boards: {end - start:.4f} seconds")

# Expert boards (16x30 with 99 mines)
# start = time.perf_counter()
# run_board(16, 30, 99, 5000)
# end = time.perf_counter()
# print(f"Time elapsed for expert boards: {end - start:.4f} seconds")  

# Beginner Density Change
# start = time.perf_counter()
# ten_percent_density = round(9 * 9 * 0.1)
# thirty_percent_density = math.ceil(9 * 9 * 0.31)
# for i in range(ten_percent_density, thirty_percent_density + 1):
#   print(f"Running {i} mines ({i / (9 * 9) * 100:.1f}%) on 9x9 board...")
#   run_board(9, 9, i, 1000)
#   print('-----------------------------------------------------------------')
# end = time.perf_counter()
# print(f"Time elapsed for beginner density change: {end - start:.4f} seconds")

# Intermediate Density Change
# start = time.perf_counter()
# for i in range(20):
#   mine_count = round(256 * (0.1 + 0.01 * i))
#   print(f"Running {mine_count} mines ({mine_count / 256 * 100:.1f}%) on 16x16 board...")
#   run_board(16, 16, mine_count, 1000)
#   print('-----------------------------------------------------------------')
# end = time.perf_counter()
# print(f"Time elapsed for intermediate density change: {end - start:.4f} seconds")

# Expert Density Change
# start = time.perf_counter()
# for i in range(1):
#   mine_count = round(480 * (0.1 + 0.01 * 20))
#   print(f"Running {mine_count} mines ({mine_count / 480 * 100:.1f}%) on 16x30 board...")
#   run_board(16, 30, mine_count, 1000)
#   print('-----------------------------------------------------------------')
# end = time.perf_counter()
# print(f"Time elapsed for expert density change: {end - start:.4f} seconds")

# Starting Position Check
start = time.perf_counter()
for i in range(9):
  for j in range(9):
    start_cell = (i, j)
    print(f"Running 9x9 board with 14 mines starting at {start_cell}...")
    run_board(9, 9, 14, 1000)
    print('-----------------------------------------------------------------')
end = time.perf_counter()
