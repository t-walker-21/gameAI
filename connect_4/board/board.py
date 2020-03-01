"""

Board definition class
"""

import numpy as np
import copy
import cv2
import graph
import time

class Board(object):
	def __init__(self):
		"""

		Initialize the board
		"""

		self.board = self.make_board()
		self.LUT = self.init_LUT()
		self.turn = 0
		self.graph_1 = graph.Graph(self.board.shape)
		self.graph_2 = graph.Graph(self.board.shape)

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
			
			if self.turn:
				self.board[row, column] = -1
				self.graph_2.add_vertex((row, column))

			else:
				self.board[row, column] = 1
				self.graph_1.add_vertex((row, column))

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

	def checkNConsecutiveVertGraph(self, player):

		if player == 1:
			return self.graph_1.dfs(player, self.board, "vert")

		else:
			return self.graph_2.dfs(player, self.board, "vert")

	def checkNConsecutiveHorizGraph(self, player):

		if player == 1:
			return self.graph_1.dfs(player, self.board, "horiz")

		else:
			return self.graph_2.dfs(player, self.board, "horiz")

	def checkNConsecutiveDiagGraph(self, player):

		if player == 1:
			return self.graph_1.dfs(player, self.board, "diag")

		else:
			return self.graph_2.dfs(player, self.board, "diag")

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

		#print (self.board)
		self.paint_board(over)

		if not over:
			print ("Player " + str(int(self.turn)) + "'s turn")

	def check_win(self, player):
		"""

		Check the board for a winner
		"""

		# Uncomment for speed check

		"""start = time.time()
		res = self.checkNConsecutiveDiagGraph(player)
		print "optimized func time: " , time.time() - start

		start = time.time()
		res = self.checkNConsecutiveDiag(4, player)
		print "ineff func time: " , time.time() - start

		print "result: ", res

		return res"""

		if self.checkNConsecutiveVertGraph(player) or self.checkNConsecutiveHorizGraph(player): #or self.checkNConsecutiveDiagGraph(player):
			return True

		return False

	def paint_board(self, over):
		canvas = np.ones((120, 120, 3)) * 255

		offsetx = 15
		offsety = 15

		mult = 15

		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j] == 0:
					continue
				elif self.board[i][j] == 1:
					canvas = cv2.circle(canvas, (int(j * mult + offsetx), int(i * mult + offsety)), 7, (0, 0, 200), -1)
				else:
					canvas = cv2.circle(canvas, (int(j * mult + offsetx), int(i * mult + offsety)), 7, (200, 0, 0), -1)


		cv2.imshow("game", canvas)
		cv2.waitKey(1 if not over else 0)
