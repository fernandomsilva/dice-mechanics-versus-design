import random

class RandomAgent:
	def __init__(self):
		pass
	
	def choose_action(self, gstate):
		return random.choice(gstate.available_actions)

class MoveGreedy:
	def __init__(self):
		pass
	
	def choose_action(self, gstate):
		if len(gstate.available_actions) == 1:
			return gstate.available_actions[0]
			
		return self.run(gstate)

	def heuristic(self, gstate, player_id):
		value = 0
		
		player = gstate.players[player_id]
		
		for pawn in player.pawns:
			if pawn.position < 0:
				value -= 10000
			else:
				value += (pawn.position) ** 2
		
		return value
		
	def run(self, gstate):
		player_id = gstate.current_player
	
		max = (None, None)
		#for move in gstate.available_actions:
		snapshot = gstate.takeSnapshot()
		for i in range(0, len(gstate.available_actions)):
			#copy = gstate.copy()
			move = gstate.available_actions[i]
			#copy.make_move(move)

			value = self.heuristic(gstate, player_id)
			if max[0] == None or value > max[0]:
				max = (value, move)
			
			gstate.loadSnapshot(snapshot)
			snapshot['die'] = gstate.die.copy() # to recreate the dice mechanics copy
		
		return max[1]

class AStarNode:
	def __init__(self, parent_move, gstate):
		self.parent_move = parent_move
		self.gstate = gstate
		
class AStar:
	def __init__(self):
		self.heuristic_limit = 100000
	
	def choose_action(self, gstate):
		if len(gstate.available_actions) == 1:
			return gstate.available_actions[0]
			
		return self.run(gstate)
	
	def heuristic(self, node):
		return 0
	
	def run(self, gstate):
		priority_queue = []
		result = None
		
		for i in range(0, len(gstate.available_actions)):
			copy = gstate.copy()
			move = copy.available_actions[i]
			copy.make_move(move)
			node = AStarNode(move, copy)

			if copy.current_player != gstate.gstate.current_player:
				return move
			
			priority_queue.append((node, self.heuristic(node)))
		
		priority_queue = sorted(priority_queue, key=lambda k:k[1], reverse=True)
		
		while priority_queue[0][1] < self.heuristic_limit and len(priority_queue) > 1:
			top_node = priority_queue[0][0]
			priority_queue = priority_queue[1:]
			
			for i in range(0, len(top_node.gstate.available_actions)):
				copy = top_node.gstate.copy()
				move = copy.available_actions[i]
				copy.make_move(move)
				if copy.current_player != top_node.gstate.current_player:
					priority_queue = [top_node] + priority_queue
					break
				
				node = AStarNode(top_node.parent_move, copy)
				
				priority_queue.append((node, self.heuristic(node)))

			priority_queue = sorted(priority_queue, key=lambda k:k[1], reverse=True)
				
		return priority_queue[0][0].parent_move