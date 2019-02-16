import random

class DiceMechanic:
	def __init__(self):
		pass
	
	def roll(self):
		pass

class Dice(DiceMechanic):
	def __init__(self, size=6):
		self.size = size
	
	def roll(self):
		return random.randint(1, self.size)