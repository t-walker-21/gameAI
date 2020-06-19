import numpy as np
import time
import os

arr_size = 9

arr = np.zeros((arr_size, arr_size))

arr[0][2] = 7
arr[0][3] = 9
arr[0][8] = 1

arr[1][1] = 2
arr[1][2] = 3
arr[1][3] = 8
arr[1][6] = 6
arr[1][7] = 7

arr[2][2] = 6
arr[2][4] = 2
arr[2][5] = 7

arr[3][1] = 7
arr[3][2] = 8
arr[3][4] = 5

arr[4][1] = 5
arr[4][3] = 2
arr[4][5] = 6
arr[4][7] = 3

arr[5][4] = 1
arr[5][6] = 9
arr[5][7] = 5

arr[6][3] = 6
arr[6][4] = 3
arr[6][6] = 8

arr[7][1] = 8
arr[7][2] = 4
arr[7][5] = 9
arr[7][6] = 2
arr[7][7] = 1

arr[8][0] = 2
arr[8][5] = 1
arr[8][6] = 3

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

def solve(arr, pos_x=0, pos_y=0):

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

if __name__ == "__main__":

	res = solve(arr)

	if res is None:
		print "no solution possible"

	else:
		print res