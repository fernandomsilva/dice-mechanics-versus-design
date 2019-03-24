import csv

class Card:
	def __init__(self, symbol, country):
		self.symbol = symbol
		self.country = country
	
	def __str__(self):
		return "COUNTRY: " + self.country + " /\ SYMBOL: " + str(self.symbol)
	
	def copy(self):
		return Card(self.symbol, self.country)

class BoardSpace:
	def __init__(self, country, continent, connections, number_of_armies=0, owner=-1):
		self.country = country
		self.continent = continent
		self.connections = connections
		self.number_of_armies = number_of_armies
		self.owner = owner
	
	def __str__(self):
		return "Continent: " + self.continent + " /\ Armies: " + str(self.number_of_armies) + " /\ Player: " + str(self.owner)
	
	def reset(self):
		self.number_of_armies = 0
		self.owner = -1

def load_deck(filepath):
	deck_list = []

	filedata = csv.DictReader(open(filepath, 'r'), delimiter=';')
	for row in filedata:
		deck_list.append(Card(row['SYMBOL'], row['COUNTRY']))

	return deck_list
	
def load_board(filepath):
	board_dict = {}

	filedata = csv.DictReader(open(filepath, 'r'), delimiter=';')
	for row in filedata:
		board_dict[row['COUNTRY']] = BoardSpace(row['COUNTRY'], row['CONTINENT'], row['CONNECTIONS'])

	return board_dict