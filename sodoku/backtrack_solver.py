import numpy as np
import time
import os

def inner_square(arr, i, j):
	grid_x = i / 3 * 3
	grid_y = j / 3 * 3

	return arr[grid_x:grid_x + 3, grid_y:grid_y + 3].flatten()


def check_constraint(arr):
	check = set()

	for i in arr:
		if i == 0:
			continue

		if i in check:
			return False

		check.add(i)

	return True

def get_empty_pos(arr):
	pos = []
	for i in range(len(arr)):
		if arr[i] == 0:
			pos.append(i)

	return pos

def solve(arr, pos_x=0, pos_y=0, arr_size=9):

	if pos_x == len(arr):
		return arr

	if arr[pos_x][pos_y] != 0:
		pos_y += 1

		if pos_y == len(arr):
			pos_y = 0
			pos_x += 1
		
		return solve(arr, pos_x, pos_y)

	for i in range(1, arr_size + 1):
		arr[pos_x][pos_y] = i

		"""
		os.system("clear")
		print arr
		print
		time.sleep(0.01)
		"""

		if check_constraint(arr[pos_x]) and check_constraint(arr[:, pos_y]) and check_constraint(inner_square(arr, pos_x, pos_y)):
			pos_y += 1

			if pos_y == len(arr):
				pos_y = 0
				pos_x += 1
			
			res = solve(arr, pos_x, pos_y)

			if not res is None:
				return res

			else:
				pos_y -= 1

				if pos_y < 0:
					pos_x -= 1
					pos_y = arr_size - 1

	arr[pos_x][pos_y] = 0
	return None