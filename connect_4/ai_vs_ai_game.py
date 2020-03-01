"""

Script to play tic tac toe game
"""

import sys
from board import board
from ai_player import player, player_2
import numpy as np
import time

b = board.Board()

difficulty1 = int(sys.argv[1])
difficulty2 = int(sys.argv[2])

bot1 = player.Player(difficulty1)
bot2 = player_2.Player(difficulty2)
turn = True

play_count = 0

while True:
	b.display_board()

	if (play_count > 35):
		#bot1.set_depth(4)
		pass

	if (turn): # Human's turn
		#move = int(raw_input("Enter your move\n"))
		move = bot1.get_move(b)

	else: # AI's turn
		tic = time.time()
		move = bot2.get_move(b)
		#move = int(raw_input("Enter your move\n"))
		toc = time.time() 
		print "the bot choose: " , move
		print "it took ", toc-tic, " seconds"

	b.place_piece(move)

	b.display_board()

	if b.check_win(1):
		print ("Player Red won!")
		b.display_board(True)
		exit()

	elif b.check_win(-1):
		print ("Player Blue won!")
		b.display_board(True)
		exit()

	turn ^= True
	play_count += 1

	"""if (play_count == 9):
		print "Tie Game!"
		b.display_board(True)
		exit()"""