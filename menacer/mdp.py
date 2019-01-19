""" Creating and updating Markov Decision Process parameters and policy

MENACER ('M'achine 'E'ducable 'N'oughts 'a'nd 'C'rosses 'E'ngine - Revived)
Author: R Mukesh (IIITDM Kancheepuram)
"""

from .board import standardForm, possibleNextStates, isWinningBoardState, stepsToStandardForm, translateMove
from math import inf, isclose

def generateBoardStates(player):
	'''Generate all possible unique states of the board'''

	if player == 'x':
		player_opponent = 'o'
		board_current_states = {'.........'}

	elif player == 'o':
		player_opponent = 'x'
		board_current_states = set([standardForm(board) for board in possibleNextStates('.........', 'x')])

	board_states = board_current_states.copy()
	
	# Generate the possible next states from current state
	while board_current_states:
		
		# generate the intermediate states of board after play by 'x'
		board_inter_states = set()
		for board_state in board_current_states:
			board_inter_states.update([standardForm(board) for board in possibleNextStates(board_state, player)])

		board_next_states = set()
		for board_state in board_inter_states:
			if isWinningBoardState(board_state, player) or board_state.find('.')<0:
				board_next_states.add(board_state)
			else:
				board_next_states.update([standardForm(board) for board in possibleNextStates(board_state, player_opponent)])

		board_states.update(board_next_states)
		board_current_states = set([board_state for board_state in board_next_states 
										if not (isWinningBoardState(board_state, 'x') or isWinningBoardState(board_state, 'o')) and board_state.find('.')>=0])

	return sorted(list(board_states))


def genRandomPolicy(board_states):
	'''Generate a random policy indicating actions for each state'''

	import random

	policy = {board_state:random.choice([i for i,xo in enumerate(board_state) if xo=='.']) 
				for board_state in board_states}
	return policy


def getNextMove(board, policy):
	'''Invoking the MENACER agent for next move based on a given policy'''

	standard_board = standardForm(board)

	# Rotate standard board 'n_rotation_ccw' times (counter-clockwise) to attain 'board' state
	n_rotation_ccw, mirrored_vertical = stepsToStandardForm(board)

	# Compute equivalent number of 'n_rotation_cw' times (clockwise) to attain 'board' state from its standard form
	n_rotation_cw = (4 - n_rotation_ccw) % 4

	standard_next_move = policy[standard_board]
	next_move = translateMove(standard_next_move, n_rotation_cw, mirrored_vertical, mirror='first')

	return next_move


def initTransitionProbs(player):
	''' Initialize tranisition probabilities among states of the board for players 'x' or 'o' '''

	if player == 'x':
		player_opponent = 'o'
		board_initial_states = {'.........'}

	elif player == 'o':
		player_opponent = 'x'
		board_initial_states = set([standardForm(board) for board in possibleNextStates('.........', 'x')])

	transition_probs = {}
	states_queue = list(board_initial_states)

	while states_queue:

		board_state = states_queue.pop(0)

		possible_actions = [pos for pos in range(9) if board_state[pos]=='.']
		transition_probs[board_state] = dict.fromkeys(possible_actions)

		for action in possible_actions:
			
			board_inter_state = standardForm(board_state[:action]+player+board_state[action+1:])
			if isWinningBoardState(board_inter_state, player) or board_inter_state.find('.') < 0:
				board_next_states = {board_inter_state}
			else:
				board_next_states = set([standardForm(board) for board in possibleNextStates(board_inter_state, player_opponent)])

			transition_probs[board_state][action] = dict.fromkeys(board_next_states, 1)
			states_queue += [board for board in board_next_states if 
								not (isWinningBoardState(board, 'x') or isWinningBoardState(board, 'o')) and board.find('.')>=0 and (board not in states_queue)]

	return transition_probs


def updateRewards(player, games, states_rewards, win_reward, loss_reward):
	''' Update rewards in the MDP of an agent from games played '''

	for game in games:
		
		if player == 'x':
			player_game = game[:-1][::2] + [game[-1]]

		elif player == 'o':
			player_game = game[1:-1][::2] + [game[-1]]

		if player_game[-1][1] is None: # game was drawed between players 'x' and 'o'
			reward = 0

		else:
			reward = win_reward if player_game[-1][1]==player else loss_reward

		for board_state,_ in player_game:
			standard_state = standardForm(board_state)
			states_rewards[standard_state][0] += 1
			states_rewards[standard_state][1] += reward

	return states_rewards


def updateTransitionProbs(player, games, transition_probs):
	''' Update the state transition probabilities in the MDP of an agent from games played '''

	for game in games:

		if player == 'x':
			player_game = game[:-1][::2] + [game[-1]]

		elif player == 'o':
			player_game = game[1:-1][::2] + [game[-1]]


		for i in range(len(player_game)-1):

			current_board_state = player_game[i][0]
			standard_current_state = standardForm(current_board_state)

			next_board_state = player_game[i+1][0]
			standard_next_state = standardForm(next_board_state)

			n_rotations_cw, mirrored_vertical = stepsToStandardForm(current_board_state)
			next_move = player_game[i][1]
			standard_next_move = translateMove(next_move, n_rotations_cw, mirrored_vertical, mirror='last')

			transition_probs[standard_current_state][standard_next_move][standard_next_state] += 1

	return transition_probs


def updatePolicy(board_states, states_values, policy, transition_probs, states_rewards, discount_factor):
	'''Update the policy (and implicitly state values) based on estimated rewards and transition probabilities using value iteration algorithm'''

	n_values_changed = True

	while n_values_changed:

		n_values_changed = 0

		for current_board_state in board_states:

			max_expected_payoff = -inf
			max_payoff_action = None

			# Determine action that maximizes pay off at current board state
			for action in transition_probs.get(current_board_state, {}):
				
				expected_payoff = 0
				for next_board_state in transition_probs[current_board_state][action]:
					expected_payoff += transition_probs[current_board_state][action][next_board_state]*states_values[next_board_state]
				expected_payoff /= sum(transition_probs[current_board_state][action].values())

				if expected_payoff > max_expected_payoff:
					max_expected_payoff = expected_payoff
					max_payoff_action = action

			if states_rewards[current_board_state][0] == 0:
				avg_state_reward = 0

			else:
				avg_state_reward = states_rewards[current_board_state][1]/states_rewards[current_board_state][0]

			state_value = avg_state_reward + discount_factor*(max_expected_payoff if max_payoff_action is not None else 0)

			if not isclose(states_values[current_board_state], state_value, rel_tol=0.001, abs_tol=0.0):
				policy[current_board_state] = max_payoff_action
				states_values[current_board_state] = state_value
				n_values_changed += 1

	return policy