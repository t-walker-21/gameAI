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
		self.board = np.zeros((3, 3))
		self.turn = 0
		self.dictionary = self.make_dict()

	def copy(self):
		"""

		Return copy of this object
		"""

		new_board = copy.deepcopy(self)
		return new_board

	def make_dict(self):
		"""

		Make the dictionary mapping from integer number to board position
		"""
		d = dict()

		d[7] = (0, 0) 
		d[8] = (0, 1)
		d[9] = (0, 2)
		d[4] = (1, 0)
		d[5] = (1, 1)
		d[6] = (1, 2)
		d[1] = (2, 0)
		d[2] = (2, 1)
		d[3] = (2, 2)

		return d

	def reset_board(self):
		"""

		Reset the game board
		"""
		self.board = np.zeros((3, 3))
		self.turn = True

	def place_piece(self, spot):
		"""

		Take in integer spot and place X or O on board if not taken
		"""

		if (spot < 1 or spot > 9):
			print ("INPUT INVALID! CHOOSE ANOTHER")
			return -1

		position = self.dictionary[spot]

		if self.board[position[0]][position[1]] != 0:
			print ("SPOT ALREADY TAKEN! CHOOSE ANOTHER")
			return -1

		self.board[position[0]][position[1]] = 1 if not self.turn else -1
		self.turn ^= True

		return 0

	def display_board(self, over=False):

		print (self.board)

		if not over:
			print ("Player " + str(int(self.turn)) + "'s turn")

	def check_win(self, player):
		"""

		Check the board for a winner
		"""

		# Vertical check
		for i in range(3):
			if (self.board[:, i] == player).all():
				return True

		# Horizontal check
		for i in range(3):
			if (self.board[i, :] == player).all():
				return True

		# Diagonal LR check
		if (self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[2][2] == player):
			return True

		# Diagonal RL check
		if (self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] == player):
			return True

		return False