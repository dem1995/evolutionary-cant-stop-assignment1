"""The best script after running the program with 26 epochs"""

#vigorous-crane
from collections import defaultdict
from src.players.Player import Player
from src.players.DSL import DSL

class Player0e26(Player):
	def __init__(self):
		self.name = 'vigorous-crane'
		self.ifclause_usecount = [0 for i in range(len(['DSL.hasWonColumn(state,a) and DSL.isStopAction(a)']))]

	def get_action(self, state):
		actions = state.available_moves()
        
		for a in actions:
			#return a
			if DSL.hasWonColumn(state,a) and DSL.isStopAction(a):
				self.ifclause_usecount[0] += 1
				return a
		return actions[0]