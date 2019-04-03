from ludo import *
import random

players = []
for i in range(0, 4):
	players.append(Player(i, [-1] * number_of_pawns_per_player))

dm = dice_mechanics.Dice(6)

gs = Gamestate(players, dm)

gs.setup()
gs.calculate_available_actions()

turn_count = 0

def lengthBoard(board):
	total = 0
	
	for space in board:
		if space != None:
			total += len(space)
	
	return total
	
def totalPawnsOnBoard(state):
	total = 0

	for player in state.players:
		for pawn in player.pawns:
			if pawn.position > 0 and pawn.position <= shared_board_size:
				total += 1
	
	return total

for i in range(0, 150):
	action = random.choice(gs.available_actions)
	gs.make_move(action)

ss = gs.takeSnapshot()
#print(gs.board)
print(lengthBoard(gs.board), totalPawnsOnBoard(gs))

for i in range(0, 50):
	action = random.choice(gs.available_actions)
	gs.make_move(action)

#print(gs.board)
print(gs)
print(gs.board)
print(lengthBoard(gs.board), totalPawnsOnBoard(gs))
gs.loadSnapshot(ss)

#print(gs.board)
print(lengthBoard(gs.board), totalPawnsOnBoard(gs))
