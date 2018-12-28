""" Representation and Transformation of Board Configurations

MENACER ('M'achine 'E'ducable 'N'oughts 'a'nd 'C'rosses 'E'ngine - Revived)
Author: R Mukesh (IIITDM Kancheepuram)
"""

def rotateBoard90CW(board):
	'''Rotate the board by 90 degrees clockwise'''

	rotated_board = ''

	for i in range(-3, 0):
		rotated_board += board[i::-3]

	return rotated_board


def mirrorBoardVertical(board):
	'''Mirror the board about the vertical axis'''

	mirrored_board = ''
	
	for i in range(0, 9, 3):
		mirrored_board += board[i:i+3][::-1]

	return mirrored_board


def convertBoardToArray(board):
	'''convert the board to an array of [-1,0,1]'''

	xo_to_num = {
		'x': 1,
		'o': -1,
		'.': 0
	}

	board_array = [xo_to_num[xo] for xo in board]
	return board_array


def convertArrayToBoard(board_array):
	'''convert the board array to board string'''

	num_to_xo = {
		1: 'x',
		-1: 'o',
		0: '.'
	}

	board = ''.join(num_to_xo[num] for num in board_array)
	return board


def compareBoardArrays(board_array1, board_array2):
	'''compare board arrays'''

	for xo1,xo2 in zip(board_array1, board_array2):
		if xo1 < xo2:
			return -1
		elif xo1 > xo2:
			return 1

	return 0


def standardForm(board):
	'''convert the board to standard form'''

	max_board_array = [-1]*9

	for i in range(4):
		
		board_array = convertBoardToArray(board)

		if(compareBoardArrays(board_array, max_board_array) > 0):
			max_board_array = board_array

		mirrored_board = mirrorBoardVertical(board)
		mirrored_board_array = convertBoardToArray(mirrored_board)

		if(compareBoardArrays(mirrored_board_array, max_board_array) > 0):
			max_board_array = mirrored_board_array

		board = rotateBoard90CW(board)				

	standard_board = convertArrayToBoard(max_board_array)
	return standard_board


def possibleNextStates(board, player):
	'''Generates possible next states for one move/player ('x' or  'o')'''
	return [board[:pos]+player+board[pos+1:] for pos in range(9) if board[pos]=='.']


def isWinningBoardState(board, player):
	'''Check if the board state is a winning board state for the player ('x' or 'o')'''

	if player == None:
		return False

	winning_streak = player*3

	if 	(
		(board[0:3] == winning_streak) or (board[3:6] == winning_streak) or (board[6:9] == winning_streak) # along horizontal lines
		or (board[0::3] == winning_streak) or (board[1::3] == winning_streak) or (board[2::3] == winning_streak) # along vertical lines
		or (board[0::4] == winning_streak) or (board[2:7:2] == winning_streak) # along two diagonals
		):
		return True

	else:
		return False


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
			if isWinningBoardState(board_state, player):
				board_next_states.add(board_state)
			else:
				board_next_states.update([standardForm(board) for board in possibleNextStates(board_state, player_opponent)])

		board_states.update(board_next_states)
		board_current_states = set([board_state for board_state in board_next_states if not (isWinningBoardState(board_state, 'x') or isWinningBoardState(board_state, 'o'))])

	return sorted(list(board_states))


def genRandomPolicy(board_states):
	'''Generate a random policy indicating actions for each state'''
	import random

	policy = {board_state:random.choice([i for i,xo in enumerate(board_state) if xo=='.']) 
				for board_state in board_states}
	return policy


def stepsToStandardForm(board):
	'''steps in converting the board to standard form'''

	max_board_array = [-1]*9

	for i in range(4):
		
		board_array = convertBoardToArray(board)

		if(compareBoardArrays(board_array, max_board_array) > 0):
			n_rotation_cw = i
			mirrored_vertical = False
			max_board_array = board_array

		mirrored_board = mirrorBoardVertical(board)
		mirrored_board_array = convertBoardToArray(mirrored_board)

		if(compareBoardArrays(mirrored_board_array, max_board_array) > 0):
			n_rotation_cw = i
			mirrored_vertical = True
			max_board_array = mirrored_board_array

		board = rotateBoard90CW(board)				

	return n_rotation_cw, mirrored_vertical


def translateMove(move, n_rotation_cw, mirrored_vertical):
	'''Return translated move for rotated and mirrored boards'''
	
	if mirrored_vertical:
		move = (2 - move%3) + (move//3)*3

	for i in range(n_rotation_cw):

		if move in range(3):
			move = 3*move+2
		elif move in range(2, 9, 3):
			move = 7 - (move-5)//3
		elif move in range(6, 9):
			move = (move-6)*3
		elif move in range(0, 9, 3):
			move = 2 - move//3

	return move


def getNextMove(board, policy):
	'''Invoking the MENACER agent for next move based on a given policy'''

	standard_board = standardForm(board)
	n_rotation_ccw, mirrored_vertical = stepsToStandardForm(board)
	n_rotation_cw = (4 - n_rotation_ccw) % 4

	standard_next_move = policy[standard_board]
	next_move = translateMove(standard_next_move, n_rotation_cw, mirrored_vertical)

	return next_move


def displayBoard(board):
	'''Display the given board configuration'''
	
	print(
			' {} | {} | {} \n'
			'---|---|---\n'
			' {} | {} | {} \n'
			'---|---|---\n'
			' {} | {} | {} '.format(*board.replace('.', ' ').upper())
		)


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
								not (isWinningBoardState(board, 'x') or isWinningBoardState(board, 'o')) and board.find('.')>=0 and board not in states_queue]

	return transition_probs