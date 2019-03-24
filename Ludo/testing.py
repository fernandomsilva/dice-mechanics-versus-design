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

for i in range(0, 150):
	action = random.choice(gs.available_actions)
	gs.make_move(action)

print(gs)