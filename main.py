"""Python program for generating Can't-Stop scripts genetically"""

import importlib
import random
import shutil
from itertools import combinations
from pathlib import Path
import coolname
import numpy as np
from src.players.DSL import DSL
from src.players.Script import Script
from src.players.scripts_independent.HandcraftedPlayer import HandcraftedPlayer
from src.tournament import PlayGames, RoundRobin, ScoresAgainstBaselinePlayers, ScoresAgainstGivenPlayer

def evolve_algorithm(popsize=25, numepochs=1, elitecount=7, childrencount=13, tourneyentrycount=7, mutationrate=0.7, testplayer=None):
	"""
	Algorithm to evolutionarily produce a script to play the board game "Can't Stop".

	Parameters:
	popsize (int): the population of scripts to consider each epoch
	elitecount (int): the number of surviving elites each epoch
	numepochs (int): the number of times the game should generate elites/mutate/run tourneys
	tourneyentrycount (int): the number of entrants to randomly sample from the population
		to enter a tournament to select "breeders"
	mutationrate (float): the chance of mutation occurring whenever scripts breed

	Returns:
	The top-performing evolved scripts
	
	Gives the top surviving scripts after numepochs iterations of the following:
	1) Randomly-generated scripts (according to DSL.py) invading the population until 
		the population count is popsize
	2) The population of scripts having a round-robin tournament, and elitecount of 
		the scripts "surviving" (excluding breeding)
	3) Random samples (retaken each tourney) of the population (of size elitecount) 
		holding childrencount tourneys (comparing scores from the earlier round-robin 
		tournament to cut down on runtime) to decide two members to breed
	3a) The victors of each tourney "breed" a child; specifically, they do so by 
		crossing over their rules to produce two children, one of which is chosen 
		for consideration and the other discarded 
		(both have equal probability of being chosen)
	3b) The chosen child from 3a has mutationrate chance of undergoing a mutation to 
		change up its rules
	4) The elites and children either enter the next round as the population prior to
		invasion, or the elites are returned from the algorithm in the order they 
		performed in the round-robin tournament (better-performing placed earlier in the 
		list)
	"""
	if testplayer == None:
		testplayer = HandcraftedPlayer()

	average_scores_against_test = []
	max_scores_against_test = []

	#Generate scripts
	scripts = []
	for i in range(popsize):
		rules = [DSL.RandomRule()]
		scripts.append(Script(rules))

	#Iterate the population, observing their performances and culling weaker members, 
	# as well as generating offspring at each iteration and allowing invaders to enter 
	# the population
	for epoch in range(1, numepochs+1):
		print(f"Epoch {epoch}/{numepochs}")

		#Clear cache
		dirpath = Path('src', 'players', 'scripts_generated')
		if dirpath.exists() and dirpath.is_dir():
			shutil.rmtree(dirpath)
		dirpath.mkdir()

		#Instantiate scripts/agents
		for index, script in enumerate(scripts):
			script.id = f"{index}e{epoch}"
			script.saveFile(str(dirpath))

		#Prepare agents
		for index, script in enumerate(scripts):
			module = importlib.import_module(f'src.players.scripts_generated.Script{index}e{epoch}')
			class_ = getattr(module, f'Player{index}e{epoch}')
			script.player = class_()

		#Get elite agents
		scores, orderedscores = RoundRobin([script.player for script in scripts], 40)
		scripts_to_save_indices = [orderedscores[i][0] for i in range(elitecount)]
		elites = [scripts[i] for i in scripts_to_save_indices]
		scriptsprime = [scripts[i] for i in scripts_to_save_indices]

		#Print score information for this round
		perf = ScoresAgainstGivenPlayer([script.player for script in scripts], testplayer, 40)
		eliteperf = [perf[i] for i in scripts_to_save_indices]
		print("Scores against each other: ", scores)
		print("Scores against test player: ", perf)
		print("Elite scores against test player: ", eliteperf)
		print("Average score against test player: ", sum(perf)/len(perf))
		print("Average elite score against test player: ", sum(eliteperf)/len(eliteperf)) 
		print("Retained indices: ", scripts_to_save_indices)
		average_scores_against_test.append(sum(eliteperf)/len(eliteperf))
		max_scores_against_test.append(max(eliteperf))

		#Remove unused if-clauses
		for script in scripts:
			ifclause_usecount = script.player.ifclause_usecount
			retainedruleindices = [index for index in range(len(script.rules)) if ifclause_usecount[index]>0]
			retainedrules = [script.rules[i] for i in retainedruleindices]
			script.rules = retainedrules #holy cow, this bug took me way too long to find. I had = rules here instead of =retainedrules

		
		while len(scriptsprime) < popsize + childrencount:
			#get top-two performing members of a tournament whose entrants are sampled 
			# from the population
			tournamententryindices = random.sample(range(len(scripts)), tourneyentrycount)
			tournamentscores = [(scripts[int(i)], scores[int(i)]) for i in tournamententryindices]
			sortedentries = list(reversed(sorted(tournamentscores, key = lambda x: x[1])))
			p1, p2 = sortedentries[0][0], sortedentries[1][0]

			#cross over those two members
			c1, c2 = Script.crossover(p1, p2)
			c = c1 if random.uniform(0, 1)<0.5 else c2

			#determine the need for mutation
			if random.uniform(0, 1)<mutationrate:
				c = Script.mutated(c)
			scriptsprime.append(c)


		#Generate invaders
		while(len(scriptsprime)<len(scripts)):
			rules = [DSL.RandomRule(), DSL.RandomRule()]
			scriptsprime.append(Script(rules))

		scripts = scriptsprime
	
	print(average_scores_against_test)
	print(max_scores_against_test)
	#return the best members of the last round-robin tournament
	return elites

if __name__ == '__main__':
	numepochs = 2
	scripts = evolve_algorithm(numepochs = numepochs, testplayer = HandcraftedPlayer())

	#Clear cache
	dirpath = Path('src', 'players', 'scripts_generated')
	if dirpath.exists() and dirpath.is_dir():
		shutil.rmtree(dirpath)
	dirpath.mkdir()

	#Save scripts
	for index, script in enumerate(scripts):
		script.id = f"{index}e{numepochs}"
		script.saveFile(str(dirpath))