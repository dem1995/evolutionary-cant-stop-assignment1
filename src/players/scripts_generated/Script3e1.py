
#hidden-pigeon
from collections import defaultdict
from src.players.Player import Player
from src.players.DSL import DSL

class Player3e1(Player):
	def __init__(self):
		self.name = 'hidden-pigeon'
		self.ifclause_usecount = [0 for i in range(len([]))]

	def get_action(self, state):
		actions = state.available_moves()
        
		for a in actions:
			#return a

			pass
		return actions[0]
