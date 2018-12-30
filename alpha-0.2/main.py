""" Agents learn "Noughts and Crosses" through self-play

MENACER ('M'achine 'E'ducable 'N'oughts 'a'nd 'C'rosses 'E'ngine - Revived)
Author: R Mukesh (IIITDM Kancheepuram)
"""

from agents import AgentX, AgentO, playNoughtsCrosses
import pickle

n_games = 10000000

agentx = AgentX()
agento = AgentO()

# Let agents play a 10 million games against one another
for i_game in range(n_games):
	games = [playNoughtsCrosses(agentx, agento)]
	agentx.learnGameplay(games)
	agento.learnGameplay(games)

# Serialize and dump the agents using pickle
agents_file = open("pretrained-agents/noughts-crosses.agents", 'wb')
agents = {'agentx': agentx, 'agento': agento}
pickle.dump(agents, agents_file)