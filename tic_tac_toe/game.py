"""

Script to play tic tac toe game
"""

import sys
from board import board

b = board.Board()

while True:
	b.display_board()

	move = int(raw_input("Enter your move\n"))

	b.place_piece(move)

	if b.check_win(1):
		print "Player 0 won!"
		b.display_board(True)
		exit()

	elif b.check_win(-1):
		print "Player 1 won!"
		b.display_board(True)
		exit()