"""

Minimax AI player
"""

import numpy as np

class Player(object):
	def __init__(self, depth):
		pass
		self.depth = depth

	def get_available_moves(self, board):
		"""

		Get all available moves for ai player
		"""

		moves = []

		for i in range(len(board)):
			if board[0][i] == 0:
				moves.append(i)

		return moves

	def set_depth(self, depth):
		self.depth = depth

	def get_move(self, board):
		"""

		Given board, compute best move
		"""

		temp_board = board.copy()


		move = self.minimax_helper(temp_board)

		return move


	def minimax_helper(self, board):

		moves = self.get_available_moves(board.board)

		move_values = []

		for move in moves:
			temp_board = board.copy()
			temp_board.place_piece(move)

			move_values.append(self.minimax(temp_board, False, 0))


		if np.random.rand(1) > 1.8:
			return np.random.choice(moves)

		best_ind = np.random.choice(np.argwhere(move_values == np.amax(move_values)).reshape(-1, ))

		return moves[best_ind]


	def minimax(self, board, maxi, depth_count):
		""""

		Minimax algorithm to determine best move
		"""

		if self.get_available_moves(board.board) == [] or self.depth == depth_count:
			# Evaluate board

			val = 0

			if (board.check_win(-1)):
				val = 1

			elif (board.check_win(1)):
				val = -1

			return val

		elif (board.check_win(-1) or board.check_win(1)):
			if board.check_win(1):
				return -1

			else:
				return 1

		else:
			moves = self.get_available_moves(board.board)

			move_values = []

			for move in moves:
				temp_board = board.copy()
				temp_board.place_piece(move)

				move_values.append(self.minimax(temp_board, maxi ^ True, depth_count + 1))

			if maxi:
				return max(move_values)

			else:
				return min(move_values)
