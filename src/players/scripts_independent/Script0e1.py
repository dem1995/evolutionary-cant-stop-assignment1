"""The best script after running the program with 1 epochs"""

#analytic-teal
from collections import defaultdict
from src.players.Player import Player
from src.players.DSL import DSL

class Player0e1(Player):
	def __init__(self):
		self.name = 'analytic-teal'
		self.ifclause_usecount = [0 for i in range(len(['DSL.isStopAction(a) and DSL.numberPositionsProgressedThisRoundColumn(state, 4) > 2 and DSL.isStopAction(a)']))]

	def get_action(self, state):
		actions = state.available_moves()
        
		for a in actions:
			#return a
			if DSL.isStopAction(a) and DSL.numberPositionsProgressedThisRoundColumn(state, 4) > 2 and DSL.isStopAction(a):
				self.ifclause_usecount[0] += 1
				return a
			pass
		return actions[0]
