
#voracious-locust
from collections import defaultdict
from src.players.Player import Player
from src.players.DSL import DSL

class Player5e1(Player):
	def __init__(self):
		self.name = 'voracious-locust'
		self.ifclause_usecount = [0 for i in range(len(['DSL.containsNumber(a, 4)']))]

	def get_action(self, state):
		actions = state.available_moves()
        
		for a in actions:
			#return a
			if DSL.containsNumber(a, 4):
				self.ifclause_usecount[0] += 1
				return a
			pass
		return actions[0]
