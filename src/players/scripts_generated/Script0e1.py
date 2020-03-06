
#spicy-chinchilla
from collections import defaultdict
from src.players.Player import Player
from src.players.DSL import DSL

class Player0e1(Player):
	def __init__(self):
		self.name = 'spicy-chinchilla'
		self.ifclause_usecount = [0 for i in range(len(['DSL.isStopAction(a) and DSL.hasWonColumn(state,a)']))]

	def get_action(self, state):
		actions = state.available_moves()
        
		for a in actions:
			#return a
			if DSL.isStopAction(a) and DSL.hasWonColumn(state,a):
				self.ifclause_usecount[0] += 1
				return a
			pass
		return actions[0]
