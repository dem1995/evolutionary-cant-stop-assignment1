import random
import numpy as np
import random
import collections
from collections import defaultdict
from itertools import combinations
from src.game import Board, Game
from multiprocessing import Pool

def RoundRobin(players, numgames):
	numplayers = len(players)

	scores = np.zeros((numplayers, numplayers))
	
	for i, j in combinations(range(numplayers), 2):
		if i != j:			
			ijresults = PlayGamesBothSides(players[i], players[j], numgames/2)
			scores[(i, j)] = ijresults[0]
			scores[(j, i)] = ijresults[1]

	# print(scores)
	averagescores = {i:sum(scores[i])/(numplayers-1) for i in range(numplayers)}
	sortedavgscores = sorted(averagescores.items(), key = lambda item: item[1])
	sortedavgscores.reverse()
	return averagescores, sortedavgscores

def ScoresAgainstBaselinePlayers(players, baselines, numgames):
	numbaselines = len(baselines)
	numplayers = len(players)
	scores = np.zeros(numplayers)

	for playernum in range(numplayers):
		curplayer = players[playernum]
		scores[playernum] = sum(PlayGamesBothSides(curplayer, baseline, 20)[0] for baseline in baselines)/numbaselines
	
	averagescores = {i:scores[i] for i in range(numplayers)}
	sortedavgscores = sorted(averagescores.items(), key = lambda item: item[1])
	sortedavgscores.reverse()
	return averagescores, sortedavgscores

def ScoresAgainstGivenPlayer(players, opponent, numgames):
	numplayers = len(players)
	scores = np.zeros(numplayers)

	for i in range(numplayers):
		results = PlayGamesBothSides(players[i], opponent, numgames)
		scores[i] = results[0]

	return scores

def PlayGamesBothSides(player1, player2, numgames):
	player1firstresults = PlayGames(player1, player2, int(numgames/2))
	player2firstresults = PlayGames(player2, player1, int(numgames/2))
	averageresultsp1 = (player1firstresults[0] + player2firstresults[1])/2
	averageresultsp2 = (player2firstresults[0] + player1firstresults[1])/2
	return (averageresultsp1, averageresultsp2)

def PlayGames(player1, player2, numgames):
	victories1 = 0
	victories2 = 0
	for _ in range(numgames):
		game = Game(n_players = 2, dice_number = 4, dice_value = 3, column_range = [2,6],
					offset = 2, initial_height = 1)
		
		is_over = False
		who_won = None
	
		number_of_moves = 0
		current_player = game.player_turn
		while not is_over:
			moves = game.available_moves()
			if game.is_player_busted(moves):
				if current_player == 1:
					current_player = 2
				else:
					current_player = 1
				continue
			else:
				if game.player_turn == 1:
					chosen_play = player1.get_action(game)
				else:
					chosen_play = player2.get_action(game)
				if chosen_play == 'n':
					if current_player == 1:
						current_player = 2
					else:
						current_player = 1
				#print('Chose: ', chosen_play)
				#game.print_board()
				game.play(chosen_play)
				#game.print_board()
				number_of_moves += 1
				
				#print()
			who_won, is_over = game.is_finished()
			
			if number_of_moves >= 200:
				is_over = True
				who_won = -1
				#print('No Winner!')
				
		if who_won == 1:
			victories1 += 1
		if who_won == 2:
			victories2 += 1
	#print(victories1, victories2)
	#print('Player 1: ', victories1 / (victories1 + victories2))
	#print('Player 2: ', victories2 / (victories1 + victories2))
	if victories1 + victories2 == 0:
		return (0, 0)
	p1victoryrate = victories1 / (victories1 + victories2)
	p2victoryrate = 1-p1victoryrate
	return (p1victoryrate, p2victoryrate)
