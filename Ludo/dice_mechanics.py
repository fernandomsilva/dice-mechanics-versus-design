import random

class DiceMechanic:
	def __init__(self):
		pass
	
	def roll(self):
		pass
	
	def copy(self):
		pass

class Dice(DiceMechanic):
	def __init__(self, size=6):
		self.size = size
	
	def roll(self):
		return random.randint(1, self.size)
	
	def copy(self):
		return Dice(self.size)

class CustomMechanic(DiceMechanic):
	def __init__(self, size, number_of_copies_of_face, number_of_reshuffle_cards, time_on_threadmill):
		self.size = size
		self.number_of_copies_of_face = number_of_copies_of_face
		self.number_of_reshuffle_cards = number_of_reshuffle_cards
		
		if number_of_copies_of_face < 1:
			self.bag = [i for i in range(1, self.size+1)]
		else:
			self.bag = [i for i in range(1, self.size+1)] * number_of_copies_of_face
		self.bag += [-1] * number_of_reshuffle_cards
		self.time_on_threadmill = time_on_threadmill
		
		random.shuffle(self.bag)
		
		self.discard = []
		self.threadmill = []
	
	def roll(self):
		if len(self.bag) <= 0:
			self.bag = self.bag + self.discard + self.threadmill
			random.shuffle(self.bag)
			self.discard = []
			self.threadmill = []
		
		result = self.bag.pop()
		
		while result == -1:
			self.bag = self.bag + self.discard + self.threadmill + [result]
			random.shuffle(self.bag)
			self.discard = []
			self.threadmill = []
			
			result = self.bag.pop()
		
		if self.time_on_threadmill > 0:
			self.threadmill.append(result)
			if self.time_on_threadmill <= len(self.threadmill):
				self.bag = self.bag + [self.threadmill[0]]
				random.shuffle(self.bag)
				
				self.threadmill = self.threadmill[1:]
		else:
			if self.number_of_reshuffle_cards < 1:
				self.bag = self.bag + [result]
				random.shuffle(self.bag)
			else:
				self.discard.append(result)
		
		return result
	
	def copy(self):
		copy = CustomMechanic(self.size, self.number_of_copies_of_face, self.number_of_reshuffle_cards, self.time_on_threadmill)
		
		copy.bag = list(self.bag)
		copy.discard = list(self.discard)
		copy.threadmill = list(self.threadmill)
		
		return copy