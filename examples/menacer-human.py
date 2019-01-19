# Add the project's root directory to sys path
from os.path import abspath, dirname
examples_path = dirname(abspath(__file__))
project_root_path = dirname(examples_path)

import sys
sys.path.insert(0, project_root_path)

''' Illustration: MENACER vs Human '''
from menacer import AgentX, AgentO, playNoughtsCrosses

# Initialize MDP Agent that plays 'X' with random policy
agentx = AgentX()
agento = 'human'

while True:
	# Simulate a game between agentx and agento
	game = playNoughtsCrosses(agentx, agento)

	# Update the MDP and policy of agentx to learn from game
	agentx.learnGameplay([game])