"""

Board definition class
"""

import numpy as np
import copy

class Board(object):
	def __init__(self):
		"""

		Initialize the board
		"""

		self.board = self.make_board()
		self.LUT = self.init_LUT()
		self.turn = 0

	def init_LUT(self, dim=7):
		lut = np.ones(dim, dtype=np.int8) * (dim - 1)
		return lut

	def make_board(self, dim=7):
		board = np.zeros((dim,dim))
		return board

	def print_board(self):
		print (self.board)

	def place_piece(self, column):

		if column > len(self.board[0]):
			return -1

		if (self.board[0][column] != 0):
			return -1

		else:
			row = self.LUT[column]
			self.LUT[column] -= 1
			
			self.board[row, column] = 1 if not self.turn else -1

		self.turn ^= True

		return 0

	def checkNConsecutiveHoriz(self, x, player):
		for i in range (len(self.board[0])):
			for j in range (len(self.board[0])):
				check = ((self.board[i, j:j + x] == player).all() and len(self.board[i, j:j + x]) == x)
				if check:
					#print ("horizontal " , str(x), " in a row at: ", i, ", " , j)
					return True

		return False
			
	def checkNConsecutiveVert(self, x, player):
		for i in range (len(self.board[0])):
			for j in range (len(self.board[0])):
				check = ((self.board[i: i + x, j] == player).all() and len(self.board[i: i + x, j]) == x)
				if check:
					#print ("vertical " , str(x), " in a row at: ", i, ", " , j)
					return True

		return False

	def checkNConsecutiveDiag(self, x, player):

		if self.checkNConsecutiveDiagLR(x, player) or self.checkNConsecutiveDiagRL(x, player):
			return True

		return False


	def stripe_lr(self, i, j, player, x):
		# stripe along the diagonal to check for winner

		count = 0

		for z in range(x):
			if (self.board[i + z][j + z] == player):
				count += 1

		if count == x:
			return True


	def stripe_rl(self, i, j, player, x):
		# stripe along the diagonal to check for winner

		count = 0

		for z in range(x):
			if (self.board[i + z][j - z] == player):
				count += 1

		if count == x:
			return True

	def checkNConsecutiveDiagLR(self, x, player):
		# loop through columns and diagonally traverse to bottom
		# hint: your starting row position is 0 ... maxRow - 4  
		# https://stackoverflow.com/questions/32770321/connect-4-check-for-a-win-algorithm

		for i in range(len(self.board[0]) - x + 1):
			for j in range(len(self.board[0]) - x + 1):
				if (self.stripe_lr(i, j, player, x)):
					#print ("diagonal " , str(x), " in a row at: ", i, ", " , j)
					return True

	def checkNConsecutiveDiagRL(self, x, player):
		# loop through columns and diagonally traverse to bottom
		# hint: your starting row position is 0 ... maxRow - 4  
		# https://stackoverflow.com/questions/32770321/connect-4-check-for-a-win-algorithm
		for i in range(len(self.board[0]) - x + 1):
			for j in range(len(self.board[0]) - x, len(self.board[0])):
				if (self.stripe_rl(i, j, player, x)):
					#print ("diagonal " , str(x), " in a row at: ", i, ", " , j)
					return True

	def copy(self):
		"""

		Return copy of this object
		"""

		new_board = copy.deepcopy(self)
		return new_board

	def reset_board(self):
		"""

		Reset the game board
		"""
		self.board = self.make_board()
		self.turn = True

	def display_board(self, over=False):

		print (self.board)

		if not over:
			print ("Player " + str(int(self.turn)) + "'s turn")

	def check_win(self, player):
		"""

		Check the board for a winner
		"""

		if self.checkNConsecutiveVert(4, player) or self.checkNConsecutiveHoriz(4, player) or self.checkNConsecutiveDiag(4, player):
			return True

		return False