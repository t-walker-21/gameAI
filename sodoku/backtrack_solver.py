"""

Function to implement Constraint Satisfication Problem backtracking algorithm

--Tevon Walker
"""

import numpy as np

def inner_square(arr, i, j):
	"""Turn i, j coordinate into a grid"""

	grid_x = i / 3 * 3
	grid_y = j / 3 * 3

	return arr[grid_x:grid_x + 3, grid_y:grid_y + 3].flatten()


def check_constraint(arr):
	""" Check alldiff constraint"""

	check = set()

	for i in arr:
		if i == 0:
			continue

		if i in check:
			return False

		check.add(i)

	return True

def get_empty_pos(arr):
	""" Gather empty positions in array"""

	pos = []
	for i in range(len(arr)):
		if arr[i] == 0:
			pos.append(i)

	return pos

def solve(arr, pos_x=0, pos_y=0, arr_size=9):
	""" Apply the backtracking CSP algorithm to solve soduko""" 

	if pos_x == len(arr):
		# If the position we're trying to assign is off the board, we're done
		return arr

	if arr[pos_x][pos_y] != 0:
		# Don't make assignments to nonzero entries

		pos_y += 1

		if pos_y == len(arr):
			# Wrap y/x if y overflows

			pos_y = 0
			pos_x += 1
		
		return solve(arr, pos_x, pos_y)

	for i in range(1, arr_size + 1):
		# Try 1-9 for assignments
		
		arr[pos_x][pos_y] = i

		if check_constraint(arr[pos_x]) and check_constraint(arr[:, pos_y]) and check_constraint(inner_square(arr, pos_x, pos_y)):
			# This variable assignment met constraints
			pos_y += 1

			if pos_y == len(arr):
				# Wrap
				pos_y = 0
				pos_x += 1
			
			# Make recursive call with new board
			res = solve(arr, pos_x, pos_y)

			if not res is None:
				# If a result was found, return it

				return res

			else:
				# The current assignment of the variable resulted in a broken constraint. Point the variable assignment pointer back one and try new assigment from domain
				pos_y -= 1

				if pos_y < 0:
					# Unwrap if y underflows

					pos_x -= 1
					pos_y = arr_size - 1

	# At this point, no assignment from the domain satisfied the constraints, so reset the variable to unassigned (0) and backtrack
	arr[pos_x][pos_y] = 0
	return None