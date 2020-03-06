"""
Class for creating scripts to play Can't Stop.
Also contains methods for crossover and mutation of these scripts.
"""
from src.players.DSL import DSL
import random
from coolname import generate_slug

class Script():
	def __init__(self, rules, id=0):
		self.rules = rules
		self.id = id
		self.name = generate_slug(2)
		self._fitness = 0
		self._matches_played = 0
	
	@staticmethod
	def crossover(script1, script2):
		"""
		Crosses over two scripts, putting the first part of each with\
		the second part of the other, and outputs both results.
		"""

		rules1 = script1.rules
		rules2 = script2.rules

		split1loc = random.randint(0, len(rules1))
		split2loc = random.randint(0, len(rules2))
		
		c1 = rules1[0:split1loc] + rules2[split2loc:]
		c2 = rules2[0:split2loc] + rules1[split1loc:]

		return Script(c1), Script(c2)
	
	@staticmethod
	def mutated(script):
		"""
		Randomly replaces with or appends to a rule another rule. 
		"""
		rules_after_mutation = []
		for rule in script.rules:
			if random.uniform(0, 1) < 0.5:
				rules_after_mutation.append(DSL.RandomRule())
			else:
				rules_after_mutation.append(rule)
				rules_after_mutation.append(DSL.RandomRule())
		return Script(rules_after_mutation)

	def toPythonScript(self):
		if_clauses = []
		for i, rule in enumerate(self.rules):
			if_clauses.append(
f"""			if {rule}:
				self.ifclause_usecount[{i}] += 1
				return a""")
		
		newline = '\n'
		script_template = \
f'''
#{self.name}
from collections import defaultdict
from src.players.Player import Player
from src.players.DSL import DSL

class Player{self.id}(Player):
	def __init__(self):
		self.name = '{self.name}'
		self.ifclause_usecount = [0 for i in range(len({self.rules}))]

	def get_action(self, state):
		actions = state.available_moves()
        
		for a in actions:
			#return a
{newline.join(if_clauses)}
			pass
		return actions[0]
'''
		return script_template

	def saveFile(self, path):
		py = self.toPythonScript()

		file = open(path + '/Script'+ str(self.id) + '.py', 'w')
		file.write(py)
		file.close()
        