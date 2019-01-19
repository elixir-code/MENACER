""" Reinforcement Learning Agent for Player X and O 

MENACER ('M'achine 'E'ducable 'N'oughts 'a'nd 'C'rosses 'E'ngine - Revived)
Author: R Mukesh (IIITDM Kancheepuram)
"""

from .board import isWinningBoardState, displayBoard
from .mdp import generateBoardStates, genRandomPolicy, getNextMove, initTransitionProbs, updateRewards, updateTransitionProbs, updatePolicy
import pickle


class AgentX:

	def __init__(self, win_reward=3, loss_reward=-1, discount_factor=0.3):

		self.win_reward = win_reward
		self.loss_reward = loss_reward
		self.discount_factor = discount_factor

		# Generate the list of all possible states
		self.board_states = generateBoardStates('x')

		# Initialise the state transition probabilities and average rewards
		self.transition_probs = initTransitionProbs('x')
		self.rewards = {board_state:[0, 0] for board_state in self.board_states} # rewards = [number of times node visited, sum of rewards]

		# Generate an initial random policy
		board_nonfinal_states = [ board_state for board_state in self.board_states 
									if not(isWinningBoardState(board_state, 'x') or isWinningBoardState(board_state, 'o')) and board_state.find('.')>=0]
		self.policy = genRandomPolicy(board_nonfinal_states)

		# Initialise each state's value function
		self.states_values = dict.fromkeys(self.board_states, 0)


	def getNextMove(self, board):
		'''Invoking the MENACER agent for next move based on its policy'''

		return getNextMove(board, self.policy)


	def learnGameplay(self, games):
		''' Update transition probabilities, rewards and policy based on played games 'games' '''

		self.transition_probs = updateTransitionProbs('x', games, self.transition_probs)
		self.rewards = updateRewards('x', games, self.rewards, self.win_reward, self.loss_reward)
		self.policy = updatePolicy(self.board_states, self.states_values, self.policy, self.transition_probs, self.rewards, self.discount_factor)


class AgentO:

	def __init__(self, win_reward=3, loss_reward=-1, discount_factor=0.3):

		self.win_reward = win_reward
		self.loss_reward = loss_reward
		self.discount_factor = discount_factor

		# Generate the list of all possible states
		self.board_states = generateBoardStates('o')

		# Initialise the state transition probabilities and average rewards
		self.transition_probs = initTransitionProbs('o')
		self.rewards = {board_state:[0, 0] for board_state in self.board_states} # rewards = [number of times node visited, sum of rewards]

		# Generate an initial random policy
		board_nonfinal_states = [ board_state for board_state in self.board_states 
									if not(isWinningBoardState(board_state, 'x') or isWinningBoardState(board_state, 'o')) and board_state.find('.')>=0 ]
		self.policy = genRandomPolicy(board_nonfinal_states)

		# Initialise states value function
		self.states_values = dict.fromkeys(self.board_states, 0)


	def getNextMove(self, board):
		'''Invoking the MENACER agent for next move based on its policy'''

		return getNextMove(board, self.policy)


	def learnGameplay(self, games):
		''' Update transition probabilities, rewards and policy based on played games 'games' '''

		self.transition_probs = updateTransitionProbs('o', games, self.transition_probs)
		self.rewards = updateRewards('o', games, self.rewards, self.win_reward, self.loss_reward)
		self.policy = updatePolicy(self.board_states, self.states_values, self.policy, self.transition_probs, self.rewards, self.discount_factor)


def playNoughtsCrosses(agentx, agento):
	'''Play a game of Noughts and Crosses using the given policy'''

	print()

	game = []

	board = '.........'
	player = None

	while (not isWinningBoardState(board, player)) and (board.find('.') >= 0):

		# Switch between players 'x' and 'o' and define initial player
		if player == None: player = 'x'
		elif player == 'x': player = 'o'
		elif player == 'o': player = 'x'

		# MENACER's play
		if player == 'x':

			if agentx == 'human':
				next_move = int(input("Enter Next Move: ").strip())
				while next_move not in range(9) or board[next_move]!='.':
					next_move = int(input("Invalid Move. Enter Next Move: ").strip())

			else:
				next_move = agentx.getNextMove(board)


		# Human's play
		elif player == 'o':
			
			if agento == 'human':
				next_move = int(input("Enter Next Move: ").strip())
				while next_move not in range(9) or board[next_move]!='.':
					next_move = int(input("Invalid Move. Enter Next Move: ").strip())

			else:
				next_move = agento.getNextMove(board)

		game.append((board, next_move))
		board = board[:next_move] + player + board[next_move+1:]

		displayBoard(board)
		print("Player '{}' plays move {}".format(player, next_move), end='\n\n')


	if isWinningBoardState(board, player):
		print("*** Player '{}' wins! ***".format(player))
		game.append((board, player))

	else:
		print("*** Match Draws ***")
		game.append((board, None))

	return game
