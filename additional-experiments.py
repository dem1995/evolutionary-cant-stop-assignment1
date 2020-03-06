from src.players.DSL import DSL
from src.players.Script import Script
from src.players.scripts_independent.Script0e1 import Player0e1 as FirstEpochPlayer
from src.players.scripts_independent.Script0e26 import Player0e26 as EvolvedPlayer
from src.players.scripts_independent.HandcraftedPlayer import HandcraftedPlayer
from src.players.scripts_independent.RandomPlayer import RandomPlayer
from src.tournament import PlayGamesBothSides, PlayGames

numgames = 5000

playernames = \
	{
		FirstEpochPlayer: "First-Epoch Player",
		EvolvedPlayer: "Evolved Player",
		HandcraftedPlayer: "Handcrafted Player",
		RandomPlayer: "Random Player"
	}

def printresults(player1, player2):
	player1name = playernames[player1]
	player2name = playernames[player2]
	player1 = player1()
	player2 = player2()
	print(f"{player1name} vs {player2name}")
	print(f"Average results for {int(numgames/2)} games each of {player1name} moving first and {player2name} moving first")
	results = PlayGamesBothSides(player1, player2, numgames)
	print(f"{player1name} winrate: {results[0]}. {player2name} winrate: {results[1]}")
	print(f"Average results for {numgames} games of {player1name} moving first against {player2name}")
	results = PlayGames(player1, player2, numgames)
	print(f"{player1name} winrate: {results[0]}. {player2name} winrate: {results[1]}")
	print(f"Average results for {numgames} games of {player2name} moving first against {player1name}")
	results = PlayGames(player2, player1, numgames)
	print(f"{player1name} winrate: {results[1]}. {player2name} winrate: {results[0]}")

print("-------------------------------------")
printresults(FirstEpochPlayer, RandomPlayer)
print("-------------------------------------")
printresults(EvolvedPlayer, RandomPlayer)
print("-------------------------------------")
printresults(HandcraftedPlayer, RandomPlayer)
print("-------------------------------------")
printresults(EvolvedPlayer, FirstEpochPlayer)
print("-------------------------------------")
printresults(HandcraftedPlayer, EvolvedPlayer)
print("-------------------------------------")