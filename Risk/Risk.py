import componentParse

import random, math, itertools

number_territories_per_continent = {}

class Player:
	def __init__(self, total_number_of_pawns, current_available_pawns, hand, owned_territory):
		self.total_number_of_pawns = total_number_of_pawns
		self.current_available_pawns = current_available_pawns
		#self.hand = dict(hand)
		self.hand = [0, 0, 0, 0, 0]
		self.owned_territory = dict(owned_territory)
	
	def copy(self):
		return Player(self.total_number_of_pawns, self.current_available_pawns, self.hand, self.owned_territory)
	
	def number_of_territories_owned_per_continent(self):
		result = {}
		
		for space in self.owned_territory:
			if space.continent not in result:
				result[space.continent] = 1
			else:
				result[space.continent] += 1
		
		return result
	
	def check_for_hand_set(self):
		non_empty_hand_slots = [x for x in self.hand if x > 0]
		
		if len(non_empty_hand_slots) < 3:
			return (0, 0, 0)
			
		combinations = list(itertools.combinations(non_empty_hand_slots))
		
		for comb in combinations:
			if (comb[0] & comb[1] & comb[2]) > 0:
				return tuple(comb)
		
		return (0, 0, 0)
	
	def remove_cards(self, hand_set):
		for card in hand_set:
			index = self.hand.index(card)
			self.hand.remove(index)

class GameState:
	def __init__(self, players, current_player, deck, board, number_of_returned_sets, current_round=None):
		self.players = list(players)
		self.current_player = current_player
		self.deck = list(deck)
		self.board = dict(board)
		self.current_round = current_round
		#self.available_cards
		self.number_of_returned_sets = number_of_returned_sets
		
		if len(number_territories_per_continent.keys()) <= 0 and len(self.board) > 1:
			for space in self.board:
				if space.continent not in number_territories_per_continent:
					number_territories_per_continent[space.continent] = 1
				else:
					number_territories_per_continent[space.continent] += 1
		
	def copy(self):
		players_copy = []
		for player in self.players:
			players_copy.append(player.copy())
			
		return GameState(players_copy, self.current_player, self.deck, self.board)

	def setup(self, deck_filepath, board_filepath):
		if len(self.players) > 2:
			starting_infantry = 40 - ((len(self.players) - 2) * 5)
	
		for player in self.players:
			player.total_number_of_pawns = starting_infantry
			player.current_available_pawns = player.total_number_of_pawns
			player.hand = {}
			player.owned_territory = {}
	
		self.current_player = random.randint(0, len(self.players) - 1)
		
		self.deck = componentParse.load_deck(deck_filepath)
		random.shuffle(self.deck)
		
		if self.board == {}:
			self.board = componentParse.load_board(board_filepath)
		else:
			for boardspace in self.board:
				boardspace.reset()

		if len(number_territories_per_continent.keys()) <= 0 and len(self.board) > 1:
			for space in self.board:
				if space.continent not in number_territories_per_continent:
					number_territories_per_continent[space.continent] = 1
				else:
					number_territories_per_continent[space.continent] += 1
				
		self.available_actions = []
		self.current_round = "occupy"
		self.empty_spaces = list(self.board.keys())
		self.number_of_returned_sets = 0
	
	def next_player(self):
		self.current_player = (self.current_player + 1) % len(self.players)
	
	def update_round(self, round):
		self.current_round = round
	
	def reinforcements_for_controled_continent(self, continent):
		if continent.lower() == "AFRICA".lower():
			return 3

		if continent.lower() == "ASIA".lower():
			return 7
			
		if continent.lower() == "AUSTRALIA".lower():
			return 2

		if continent.lower() == "EUROPE".lower():
			return 5

		if continent.lower() == "NORTH AMERICA".lower():
			return 5

		if continent.lower() == "SOUTH AMERICA".lower():
			return 2
	
	def reinforcements_per_returned_sets(self, number_of_returned_sets):
		if number_of_returned_sets == 0:
			return 4
		elif number_of_returned_sets == 1:
			return 6
		elif number_of_returned_sets == 2:
			return 8
		else:
			return (number_of_returned_sets - 1) * 5
			
	def calculate_reinforcements(self):
		result = 0
		player = self.players[self.current_player]
	
		# OWNED TERRITORIES
		owned_spaces = [x for x in player.owned_territory if player.owned_territory[x] == True]
		total_owned_spaces = len(owned_spaces)
		
		result += math.floor(float(total_owned_spaces) / 3.0)
		if result < 3:
			result = 3
		
		# CONTROLED CONTINENTS
		player_territories_per_continent = player.number_of_territories_owned_per_continent()
		for continent in player_territories_per_continent:
			if player_territories_per_continent[continent] == number_territories_per_continent[continent]:
				result += self.reinforcements_for_controled_continent(continent)
		
		# SET IN HAND
		hand_set = player.check_for_hand_set()
		if hand_set[0] != 0:
			result += self.reinforcements_per_returned_sets(self.number_of_returned_sets)
			self.number_of_returned_sets += 1
			player.remove_cards(hand_set)
		
		return result
	
	def calculate_available_actions(self):
		self.available_actions = []
		player = self.players[self.current_player]
		
		if self.current_round == "occupy":
			for space in self.empty_spaces:
				self.available_actions.append(("occupy", space))

		elif self.current_round == "initial_reinforcements" or self.current_round == "reinforcements":
			owned_spaces = [x for x in player.owned_territory if player.owned_territory[x] == True]
			for space in owned_spaces:
				self.available_actions.append(("reinforce", [space, 1]))

		#elif self.current_round == "reinforcements":
		#	owned_spaces = [x for x in player.owned_territory if player.owned_territory[x] == True]
		#	for space in owned_spaces:
		#		self.available_actions.append(("reinforce", [space, 1]))
		#
		#	#number_of_reinforcements = self.calculate_reinforcements()
		
		else:
			pass
	
	def make_move(self, move):
		action = move[0]
		parameter = move[1]
		player = self.players[self.current_player]
		
		if action == "occupy":
			self.board[parameter].owner = self.current_player
			self.board[parameter].number_of_armies = 1
			player.current_available_pawns -= 1
			player.owned_territory[parameter] = True
			self.empty_spaces.remove(parameter)
			
			if len(self.empty_spaces) <= 0:
				self.update_round("initial_reinforcements")
			self.next_player()
			self.calculate_available_actions()
			
		elif action == "reinforce":
			space = parameter[0]
			army_count = parameter[1]
			
			self.board[space].number_of_armies += army_count
			player.current_available_pawns -= army_count
			
			if self.current_round == "initial_reinforcements":
				end_flag = True
				for p in self.players:
					if p.current_available_pawns > 0:
						end_flag = False
						break
						
				if end_flag:
					self.update_round("reinforcements")
					reinforcements = self.calculate_reinforcements()
				
				self.next_player()
				if self.current_round == "reinforcements":
					self.players[self.current_player].total_number_of_pawns += reinforcements
					self.players[self.current_player].current_available_pawns += reinforcements
			
			elif self.current_round == "reinforcements":
				if player.current_available_pawns <= 0:
					self.update_round("combat")
			
			self.calculate_available_actions()
		else:
			pass