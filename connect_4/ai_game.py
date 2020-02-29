"""

Script to play tic tac toe game
"""

import sys
from board import board
from ai_player import player
import numpy as np
import time

b = board.Board()

difficulty = int(sys.argv[1])

bot = player.Player(difficulty)
turn = False

play_count = 0

while True:
	b.display_board()

	if (turn): # Human's turn
		move = int(raw_input("Enter your move\n"))

	else: # AI's turn
		tic = time.time()
		move = bot.get_move(b)
		toc = time.time() 
		print "the bot choose: " , move
		print "it took ", toc-tic, " seconds"

	b.place_piece(move)

	if b.check_win(1):
		print ("Player 0 won!")
		b.display_board(True)
		exit()

	elif b.check_win(-1):
		print ("Player 1 won!")
		b.display_board(True)
		exit()

	turn ^= True
	play_count += 1

	"""if (play_count == 9):
		print "Tie Game!"
		b.display_board(True)
		exit()"""