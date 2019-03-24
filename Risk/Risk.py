import componentParse

import random

class Player:
	def __init__(self, total_number_of_pawns, current_available_pawns, hand, owned_territory):
		self.total_number_of_pawns = total_number_of_pawns
		self.current_available_pawns = current_available_pawns
		self.hand = dict(hand)
		self.owned_territory = dict(owned_territory)
	
	def copy(self):
		return Player(self.total_number_of_pawns, self.current_available_pawns, self.hand, self.owned_territory)

class GameState:
	def __init__(self, players, current_player, deck, board):
		self.players = list(players)
		self.current_player = current_player
		self.deck = list(deck)
		self.board = dict(board)
		
	def copy(self):
		players_copy = []
		for player in self.players:
			players_copy.append(player.copy())
			
		return GameState(players_copy, self.current_player, self.deck, self.board)

	def setup(self, deck_filepath, board_filepath):
		if len(self.players) > 2:
			total_infantry = 40 - ((len(self.players) - 2) * 5)
	
		for player in self.players:
			player.total_number_of_pawns = total_infantry
			player.current_available_pawns = player.total_number_of_pawns
			player.hand = {}
			player.owned_territory = {}
	
		self.current_player = random.randint(0, len(self.players) - 1)
		
		self.deck = componentParse.load_deck(deck_filepath)
		
		if self.board == {}:
			self.board = componentParse.load_board(board_filepath)
		else:
			for boardspace in self.board:
				boardspace.reset()
	
	