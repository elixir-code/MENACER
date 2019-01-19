# Add the project's root directory to sys path
from os.path import abspath, dirname
examples_path = dirname(abspath(__file__))
project_root_path = dirname(examples_path)

import sys
sys.path.insert(0, project_root_path)

''' Illustration: MENACER vs MENACER '''
from menacer import AgentX, AgentO, playNoughtsCrosses

# Initialize MDP Agents that plays 'X' and 'O' with random policies
agentx = AgentX()
agento = AgentO()

# Define the number games to be simulated
n_games = 1000

for i_game in range(n_games):

	# Simulate a game between agentx and agento
	game = playNoughtsCrosses(agentx, agento)

	# Update the MDP and policy of agents to learn from game
	agentx.learnGameplay([game])
	agento.learnGameplay([game])