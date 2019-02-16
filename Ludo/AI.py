import random

class RandomAgent:
	def __init__(self):
		pass
	
	def choose_action(self, list_of_actions):
		return random.choice(list_of_actions)