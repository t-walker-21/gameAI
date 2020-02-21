"""

Minimax AI player
"""

import numpy as np

class Player(object):
	def __init__(self):
		self.dict = self.make_dict()

	def make_dict(self):
		"""

		Make the dictionary mapping from integer number to board position
		"""
		d = dict()

		d[(0, 0)] = 7 
		d[(0, 1)] = 8
		d[(0, 2)] = 9
		d[(1, 0)] = 4
		d[(1, 1)] = 5
		d[(1, 2)] = 6
		d[(2, 0)] = 1
		d[(2, 1)] = 2
		d[(2, 2)] = 3

		return d

	def get_available_moves(self, board):
		"""

		Get all available moves for ai player
		"""

		moves = []

		for i in range(3):
			for j in range(3):
				if board[i][j] == 0:
					moves.append(self.dict[(i,j)])

		return moves


	def get_move(self, board):
		"""

		Given board, compute best move
		"""

		#possible_moves = self.get_available_moves(board.board)

		temp_board = board.copy()


		move = self.minimax_helper(temp_board)

		return move


	def minimax_helper(self, board):

		moves = self.get_available_moves(board.board)

		move_values = []

		for move in moves:
			temp_board = board.copy()
			temp_board.place_piece(move)

			move_values.append(self.minimax(temp_board, False))


		if np.random.rand(1) > 1.8:
			return np.random.choice(moves)

		return moves[np.argmax(move_values)]


	def minimax(self, board, maxi):
		""""

		Minimax algorithm to determine best move
		"""

		if self.get_available_moves(board.board) == []:
			# Evaluate board

			val = 0

			if (board.check_win(-1)):
				val = -1

			elif (board.check_win(1)):
				val = 1

			return val

		elif (board.check_win(-1) or board.check_win(1)):
			if board.check_win(1):
				return 1

			else:
				return -1

		else:
			moves = self.get_available_moves(board.board)

			move_values = []

			for move in moves:
				temp_board = board.copy()
				temp_board.place_piece(move)

				move_values.append(self.minimax(temp_board, maxi ^ True))

			if maxi:
				return max(move_values)

			else:
				return min(move_values)
