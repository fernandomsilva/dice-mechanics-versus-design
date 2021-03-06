import random
import dice_mechanics
from AI import *

import os

number_of_players = 4
number_of_pawns_per_player = 4
standard_board_side_size = 13
shared_board_size = standard_board_side_size * 4
private_board_size = 6

def save_log(filename, text):
	output_file = open(filename, 'a')
	output_file.write(text + "\n")
	output_file.close()

def log_full_game(filename, move_log):
	output_file = open(filename, 'w')
	output_file.write("Player,move,pawn,value\n")
	pawn_mapping = {}
	pawn_count = 1
	for move in move_log:
		pawn = move.pawn
		if pawn != None:
			if id(pawn) not in pawn_mapping:
				pawn_mapping[id(pawn)] = pawn_count
				pawn_count += 1
			
			pawn = pawn_mapping[id(pawn)]
		output_file.write(str(move.player_id) + "," + str(move.move) + "," + str(pawn) + "," + str(move.value) + "\n")
	output_file.close()

class Pawn:
	def __init__(self, position, player_id):
		self.position = position
		self.owner_id = player_id
	
	def __str__(self):
		return "Pawn in pos " + str(self.position)
	
	def copy(self):
		return Pawn(self.position, self.owner_id)
		

class Player:
	def __init__(self, id, pawn_positions):
		self.id = id
		self.pawns = []
		
		for i in range(0, number_of_pawns_per_player):
			self.pawns.append(Pawn(pawn_positions[i], id))
	
	def __str__(self):
		pawns_str = ""
		for pawn in self.pawns:
			pawns_str = pawns_str + str(pawn) + " /\ "
		return "Player " + str(self.id) + " <" + pawns_str + ">"
		
	def pawn_position_list(self):
		pawn_positions = []
		
		for i in range(0, len(self.pawns)):
			pawn_positions.append(self.pawns[i].position)
		
		return pawn_positions
	
	def copy(self):	
		return Player(self.id, self.pawn_position_list())
	
	def pawns_in_base(self):
		result = []
	
		for pawn in self.pawns:
			if pawn.position == -1:
				result.append(pawn)
		
		return result
	
	
class Move:
	def __init__(self, move, player_id, pawn, value):
		self.move = move
		self.player_id = player_id
		self.pawn = pawn
		self.value = value
	
	def __str__(self):
		action = self.move
		pawn = self.pawn
		if pawn == None:
			pawn = " None "
		value = self.value
		if value == 0:
			value = " None"
		
		if action == None:
			return "Player " + str(self.player_id) + " used NO move"
		
		return "Player " + str(self.player_id) + " used the move " + action + " with pawn " + str(pawn) + " and got " + str(value)
	
	def copy(self):
		return Move(self.move, self.player_id, self.pawn, self.value)
		
		
class Gamestate:
	def __init__(self, players, dice_mechanic):
		self.players = []
		
		for i in range(0, number_of_players):
			self.players.append(players[i].copy())
		
		self.board_size_player_full = shared_board_size + private_board_size
		self.board = [None] * (shared_board_size + 1) # Position 0 is special
		self.die = dice_mechanic.copy()
		#self.blocked_spaces = []
		self.result = []
		
		self.current_player = -1
		self.current_rolls_in_a_row = 0
		self.available_actions = []
		self.move_history = []
	
	'''
	def copy_of_move_history(self, gs_copy):
		result = []	
		
		for m in self.move_history:
			#result.append(m.copy())
			if m.pawn != None:
				pawn_owner = m.pawn.owner_id
				index_pawn_for_player = self.players[pawn_owner].pawns.index(m.pawn)
				
				pawn = gs_copy.players[pawn_owner].pawns[index_pawn_for_player]
				#print(m.pawn.owner_id)
				#print(self.players[pawn_owner].pawns)
			else:
				pawn = None
			
			result.append(Move(m.move, m.player_id, pawn, m.value))
		
		return result
	
	def copy_of_board(self, gs_copy):
		result = []
		
		pawn_association_table = {}
		for i in range(0, len(self.players)):
			for j in range(0, len(self.players[i].pawns)):
				pawn_association_table[self.players[i].pawns[j]] = gs_copy.players[i].pawns[j]

		for entry in self.board:
			if entry == None:
				result.append(None)
			else:
				new_entry = []
				for pawn in entry:
					new_entry.append(pawn_association_table[pawn])
				
				result.append(new_entry)
		
		return result
	
	
	def copy(self):
		gamestate_copy = Gamestate(self.players, self.die)
		gamestate_copy.board = self.copy_of_board(gamestate_copy)
		gamestate_copy.result = list(self.result)
		gamestate_copy.current_player = self.current_player
		gamestate_copy.current_rolls_in_a_row = self.current_rolls_in_a_row
		gamestate_copy.move_history = self.copy_of_move_history(gamestate_copy)#[move.copy() for move in self.move_history]
		gamestate_copy.calculate_available_actions()
		
		return gamestate_copy
	'''
	
	def takeSnapshot(self):
		snapshot = {}
		
		snapshot['die'] = self.die.copy()
		snapshot['result'] = len(self.result)
		snapshot['current_player'] = self.current_player
		snapshot['current_rolls_in_a_row'] = self.current_rolls_in_a_row
		snapshot['move_history'] = len(self.move_history)
		snapshot['pawns'] = {}
		
		for player in self.players:
			if player.id not in snapshot['pawns']:
				snapshot['pawns'][player.id] = {}
			
			for i in range(0, len(player.pawns)):
				snapshot['pawns'][player.id][i] = player.pawns[i].position
		
		return snapshot
	
	def loadSnapshot(self, snapshot): #Only loads games with the same amount of players and pawns as it is setup
		self.die = snapshot['die']
		self.result = self.result[:snapshot['result']]
		self.current_player = snapshot['current_player']
		self.current_rolls_in_a_row = snapshot['current_rolls_in_a_row']
		self.move_history = self.move_history[:snapshot['move_history']]

		self.board = []
		self.board = [None] * (shared_board_size + 1)
		
		for player_id in snapshot['pawns']:
			player = self.players[player_id]
			
			for pawn_index in snapshot['pawns']:
				pawn = player.pawns[pawn_index]
				
				pawn.position = snapshot['pawns'][player_id][pawn_index]
				
				if pawn.position > 0 and pawn.position <= shared_board_size:
					pawn_actual_position = ((pawn.position + standard_board_side_size * player_id) % (shared_board_size + 1))
					if (pawn.position + standard_board_side_size * player_id) > shared_board_size:
						pawn_actual_position += 1
					
					if pawn_actual_position > 0:
						if self.board[pawn_actual_position] == None:
							self.board[pawn_actual_position] = [pawn]
						else:
							self.board[pawn_actual_position].append(pawn)

		self.calculate_available_actions()
	
	def __str__(self):
		result = ""
		result += "Full Board Size: " + str(self.board_size_player_full) + " (" + str(shared_board_size) + "+" + str(private_board_size) + ")"
		result += "\n\n"
		for player in self.players:
			result += str(player) + "\n"
		result += "\n"
		result += "Result: " + str(self.result)
		result += "\n"
		result += "-------------------------------------------------------------"
		result += "\n\n"
		
		return result
	
	def setup(self):
		for player in self.players:
			player = Player(player.id, [-1] * number_of_pawns_per_player)
	
		self.current_player = random.choice(range(0, number_of_players))
	
		self.board = [None] * (shared_board_size + 1) # Position 0 is special
		#self.blocked_spaces = []
		self.current_rolls_in_a_row = 0
		self.result = []
		self.available_actions = []
		self.move_history = []
	
	def check_if_pawn_can_move(self, pawn, number_of_steps):
		final_position = pawn.position + number_of_steps
		
		if final_position > self.board_size_player_full + 1:
			return False
		
		actual_position = ((pawn.position + standard_board_side_size * pawn.owner_id) % (shared_board_size + 1))
		if (pawn.position + standard_board_side_size * pawn.owner_id) > shared_board_size:
			actual_position += 1
		
		final_actual_position = (((pawn.position + number_of_steps) + standard_board_side_size * pawn.owner_id) % (shared_board_size + 1))
		if ((pawn.position + number_of_steps) + standard_board_side_size * pawn.owner_id) > shared_board_size:
			final_actual_position += 1
		
		if actual_position > final_actual_position:
			traveled_board_area = self.board[actual_position+1:] + self.board[:final_actual_position+1]
		else:
			traveled_board_area = self.board[actual_position+1:final_actual_position+1]
		
		for position in traveled_board_area:
			if position != None:
				if position[0].owner_id != pawn.owner_id and len(position) > 1:
					return False
		
		return True
	
	def board_string(self):
		result = ""
		template = "xx_x/xx_x/xx_x/xx_x"
		
		for i in range(1, len(self.board)):
			if self.board[i] == None:
				result += template + " | "
			else:
				temp = template
				for y in self.board[i]:
					temp = temp.replace("xx_x", str(id(y))[-2:] + "_" + str(y.owner_id), 1)
				result += temp + " | "
		
		return result
	
	def make_move(self, action):
		if (action.move == "Dice Roll"):
			result = self.die.roll()
			self.current_rolls_in_a_row += 1
			self.move_history.append(Move(action.move, action.player_id, None, result))
			self.calculate_available_actions()
		elif (action.move == "Set Pawn"):
			action.pawn.position = 0
			self.move_history.append(Move(action.move, action.player_id, action.pawn, 0))
			self.calculate_available_actions()
		elif (action.move == "Move"):
			#save_log("bug.txt", "------------\nBoard1: " + self.board_string())
			#save_log("bug.txt", "Pawn: " + str(id(action.pawn))[-2:] + "_" + str(action.pawn.owner_id) + " /\ Pos: " + str(action.pawn.position) + " /\ Steps: " + str(action.value))

			if action.pawn.position <= shared_board_size and action.pawn.position > 0:
				actual_position = ((action.pawn.position + standard_board_side_size * self.current_player) % (shared_board_size + 1))
				if (action.pawn.position + standard_board_side_size * self.current_player) > shared_board_size:
					actual_position += 1
				if len(self.board[actual_position]) == 1:
					self.board[actual_position] = None
				else:
					self.board[actual_position].remove(action.pawn)
			action.pawn.position += action.value
			if action.pawn.position <= shared_board_size:
				actual_position = ((action.pawn.position + standard_board_side_size * self.current_player) % (shared_board_size + 1))
				if (action.pawn.position + standard_board_side_size * self.current_player) > shared_board_size:
					actual_position += 1
				if self.board[actual_position] != None: #and len(self.board[actual_position]) > 0:
					if self.board[actual_position][0].owner_id == action.pawn.owner_id:
						self.board[actual_position].append(action.pawn)
						#save_log("bug.txt", "APPEND " + str(len(self.board[actual_position])))
					elif self.board[actual_position][0].owner_id != action.pawn.owner_id and action.pawn.position <= shared_board_size:
						self.board[actual_position][0].position = -1
						#save_log("bug.txt", str(id(self.board[actual_position][0]))[-2:] + "_" + str(self.board[actual_position][0].owner_id) + "  " + str(self.board[actual_position][0].position))
						self.board[actual_position] = [action.pawn]
				else:
					#save_log("bug.txt", "WAS NONE")
					self.board[actual_position] = [action.pawn]
			self.move_history.append(Move(action.move, action.player_id, action.pawn, action.value))
			if self.check_finish(self.current_player):
				self.result.append(self.current_player)
				if len(self.result) == (number_of_players - 1):
					for i in range(0, number_of_players):
						if i not in self.result:
							self.result.append(i)
							break
			#save_log("bug.txt", "Board2: " + self.board_string() + "\n------------")
			self.calculate_available_actions()
		else: #Made NO move
			self.current_player = (self.current_player + 1) % number_of_players
			while self.check_finish(self.current_player):
				self.current_player = (self.current_player + 1) % number_of_players
	
			self.move_history.append(Move(action.move, action.player_id, None, 0))
			self.current_rolls_in_a_row = 0
			self.calculate_available_actions()	
			
	def calculate_available_actions(self):
		self.available_actions = []
	
		if len(self.move_history) < 1:
			self.available_actions.append(Move("Dice Roll", self.current_player, None, 0))
		else:
			last_move = self.move_history[-1]
			if last_move.move == "Dice Roll" and last_move.player_id == self.current_player:
				if last_move.value == 6:
					pawns_in_base = self.players[self.current_player].pawns_in_base()
					if len(pawns_in_base) > 0:
						for pawn in pawns_in_base:
							self.available_actions.append(Move("Set Pawn", self.current_player, pawn, 0))
		
			if last_move.player_id != self.current_player:
				self.available_actions.append(Move("Dice Roll", self.current_player, None, 0))
		
			else:
				if last_move.move != "Dice Roll" and self.current_rolls_in_a_row == 3:
					self.available_actions = [Move(None, self.current_player, None, 0)]
				
				elif (last_move.move == "Set Pawn" or (last_move.move == "Move" and last_move.value == 6)) and self.current_rolls_in_a_row < 3:
					self.available_actions.append(Move("Dice Roll", self.current_player, None, 0))

				elif last_move.move == "Dice Roll":
					current_player = self.players[self.current_player]
					for pawn in current_player.pawns:
						if pawn.position < self.board_size_player_full + 1 and pawn.position > -1:
							if self.check_if_pawn_can_move(pawn, last_move.value):
								self.available_actions.append(Move("Move", self.current_player, pawn, last_move.value))

			if self.available_actions == []:
				self.available_actions = [Move(None, self.current_player, None, 0)]
	
	def check_finish(self, player_id):
		player = self.players[player_id]
		
		for pawn in player.pawns:
			if pawn.position < self.board_size_player_full + 1:
				return False
		
		return True

class Gameloop:
	def __init__(self, game, AIs, dice_mec):
		if game == None:
			players = []
			for i in range(0, number_of_players):
				players.append(Player(i, [-1] * number_of_pawns_per_player))
			
			self.gamestate = Gamestate(players, dice_mec)#dice_mechanics.Dice(6))
			
		self.AIs = AIs
	
	def gameloop(self):
		action = self.AIs[self.gamestate.current_player].choose_action(self.gamestate)
		self.gamestate.make_move(action)
		#input()

	def run_game(self):
		self.gamestate.setup()
		self.gamestate.calculate_available_actions()
		
		turn_count = 0
		
		while len(self.gamestate.result) < number_of_players:
			self.gameloop()
			turn_count += 1
			#if (turn_count % 50) == 0:
			#	save_log("output.txt", "Turn " + str(turn_count) + "\n" + str(self.gamestate))
			#	print(turn_count)
		
		#print(self.gamestate.result)
		
		return self.gamestate

#results = []
#t = 1000
#for i in range(0, t):
#	gl = Gameloop(None, [MoveGreedy(), RandomAgent(), RandomAgent(), RandomAgent()], dice_mechanics.Dice(6))
#	results.append(gl.run_game().result)
#
#wins = [0, 0, 0, 0]
#for r in results:
#	wins[r.index(0)] += 1
#
#print([float(x)/float(t) for x in wins])

#print(runNLudoGames(10))
#if os.path.exists("bug.txt"):
#	os.remove("bug.txt")
#if os.path.exists("output.txt"):
#	os.remove("output.txt")
	
#output_file = open("results.csv", 'w')
#for r in results:
#	output_file.write(str(r) + '\n')
#output_file.close()

#log_full_game("moves_history.csv", gl.gamestate.move_history)