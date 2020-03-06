# Evolving "Can't-Stop" Agents
## Introduction
This repository contains code for generating artificial intelligence agents for the game "Can't Stop". "Can't Stop" is a game created by Sid Sackson in 1980 [[1](https://en.wikipedia.org/wiki/Can%27t_Stop_(board_game))]; at the time of writing, a version of the game can be played at [Board Game Arena](https://en.boardgamearena.com/gamepanel?game=cantstop).

This was a project for the Winter 2020 Explainable AI Course taught at the University of Alberta by Dr. Levis.

## Agent Creation - `Script.py` and `DSL.py`
Agents are created using a context free grammar as specified in `Script.py` and `DSL.py`. The CFG generates if-clauses that check for conditions on the "Can't Stop" board to determine what actions to take next. The possible actions themselves are specified by <DSL.py>, and call actions in `game.py`, which hosts the game itself. 

## Agent Evolution - `main.py`
  Algorithm to evolutionarily produce a script to play the board game "Can't Stop". It gives the top surviving agents after a number of evolutionary iterations as described as follows.
  
0. Randomly generates scripts to compose the population until the population has reached its maximum size
1. If we are not in the first epoch, we generate random "invader" scripts to fill the gap in the population left by the previous round until it has reached its maximum size
2. The population of scripts undergoes a round-robin tournament (specified in `tournament.py`, and some number of the scripts "survives"; these are referred to as the elites of this round
3. Random samples (retaken each tourney) of the population (including the non-elites) participate in tourneys (comparing scores from the earlier round-robin tournament to cut down on runtime) to decide two members to breed
   - The victors of each tourney "breed" a child; specifically, they do so by crossing over their rules to produce two children, one of which is chosen for consideration and the other discarded (both have equal probability of being chosen)
   - The chosen child from 3.1, with a user-specified probability, undergoes a mutation to change up its rules
4. The elites and children enter the next round as the population prior to invasion if we have not reached the last epoch. Otherwise, the elites are returned by the program.

Additionally, at each epoch of the algorithm, the population members' performances are compared to some provided baseline script.

## Additional Agent Evaluation - `report-experiments.py`
  Compares the results of the agents in the `scripts-independent` folder. These include some scripts taken from a previous run of agent evolution, as well as a random agent and a hand-crafted agent
