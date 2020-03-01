"""

Implementation of simple graph for quick win check, no edge implemented at instatiation but at dfs time
"""

import numpy

class Graph(object):
	def __init__(self, board_shape):
		self.vertices = []
		self.board_shape = board_shape

	def add_vertex(self, node):
		self.vertices.append(node)

	def get_neighbors(self, mode, vertex, player, board):

		neighbors = []
		row = vertex[0]
		col = vertex[1]

		if mode == "vert":
			if (vertex[0] != 0):

				if (board[row - 1][col] == player):
					neighbors.append((row - 1, col))

			if (vertex[0] != self.board_shape[0] - 1):
				if (board[row + 1][col] == player):
					neighbors.append((row + 1, col))

		elif mode == "horiz":
			if (vertex[1] != 0):
				if (board[row][col - 1] == player):
					neighbors.append((row, col - 1))

			if (vertex[1] != self.board_shape[1] - 1):
				if (board[row][col + 1] == player):
					neighbors.append((row, col + 1))

		else:
			if (vertex[0] != 0 and vertex[0] != self.board_shape[0] - 1):
				if (board[row - 1][col - 1] == player):
					neighbors.append((row - 1, col - 1))

			
			

			if (board[row + 1][col + 1] == player):
				neighbors.append((row + 1, col + 1))



		return neighbors 


	def dfs(self, player, board, mode, num=4):
		
		visited = []

		#print "inside dfs"

		queue = []

		for vertex in self.vertices:

			count = 0
			queue.append(vertex)

			#print queue

			while len(queue) > 0:

				node = queue.pop(0)

				neighbors = self.get_neighbors(mode, node, player, board)

				#print "the neighbors of: " , node, " are: " , neighbors

				for neigh in neighbors:
					if not (neigh in visited):
						queue.append(neigh)

				visited.append(node)
				count += 1

			#print "count is:" , count

			if count == num:
				return True

		return False




	def dfs_horizontal(self):
		pass

	def dfs_diag_rl(self):
		pass

	def dfs_diag_lr(self):
		pass