from src.players.Player import Player
from src.players.DSL import DSL

class HandcraftedPlayer(Player):
	def get_action(self, state):
		actions = state.available_moves()
		for a in actions:
			if DSL.actionWinsColumn(state,a):
				return a
		for a in actions:
			if DSL.hasWonColumn(state,a) and DSL.isStopAction(a):
				return a
		for a in actions:
			if DSL.isDoubles(a):
				return a
		return actions[0]