""" Project MENACER ('M'achine 'E'ducable 'N'oughts 'a'nd 'C'rosses 'E'ngine - Revived)
Motto: I challange you ...

Author: R Mukesh, IIITDM Kancheepuram
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


def generateBoardStates():
	'''Generate all possible unique states of the board'''

	board_states = set(['.........'])
	board_current_states = {'.........'}
	
	# Generate the possible next states from current state
	while board_current_states:
		
		# generate the intermediate states of board after play by 'x'
		board_inter_states = set()
		for board_state in board_current_states:
			board_inter_states.update([standardForm(board) for board in possibleNextStates(board_state, 'x')])

		board_next_states = set()
		for board_state in board_inter_states:
			if isWinningBoardState(board_state, 'x'):
				board_next_states.add(board_state)
			else:
				board_next_states.update([standardForm(board) for board in possibleNextStates(board_state, 'o')])

		board_states.update(board_next_states)
		board_current_states = set([board_state for board_state in board_next_states if not (isWinningBoardState(board_state, 'x') or isWinningBoardState(board_state, 'o'))])

	return sorted(list(board_states))


def genRandomPolicy(board_states):
	'''Generate a random policy indicating actions for each state'''
	import random

	policy = {board_state:random.choice([i for i,xo in enumerate(board_state) if xo=='.']) 
				for board_state in board_states}
	return policy


def displayBoard(board):
	'''Display the given board configuration'''
	
	print(
			' {} | {} | {} \n'
			'---|---|---\n'
			' {} | {} | {} \n'
			'---|---|---\n'
			' {} | {} | {} '.format(*board.replace('.', ' ').upper())
		)


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


def playNoughtsCrosses(policy):
	'''Play a game of Noughts and Crosses using the given policy'''

	board = '.........'

	player = None

	while (not isWinningBoardState(board, player)) and (board.find('.') >= 0):

		# Switch between players 'x' and 'o' and define initial player
		if player == None: player = 'x'
		elif player == 'x': player = 'o'
		elif player == 'o': player = 'x'

		# MENACER's play
		if player == 'x':
			next_move = getNextMove(board, policy)
			board = board[:next_move] + 'x' + board[next_move+1:]

		# Human's play
		elif player == 'o':
				

			next_move = int(input("Enter move: ").strip())
			
			while not (next_move in range(9) and board[next_move] == '.'):
				print("Invalid move. Enter move: ", end='')
				next_move = int(input().strip())

			board = board[:next_move] + 'o' + board[next_move+1:]

		displayBoard(board)
		print("Player '{}' plays move {}".format(player, next_move), end='\n\n')


	if isWinningBoardState(board, player):
		print("Player '{}' wins!".format(player))

	else:
		print("Match Draws ...")

if __name__ == '__main__':

	print("MENACER - Machine Educable Noughts And Crosses Engine Revived")

	# Generate a list of all possible states
	board_states = generateBoardStates()

	# Generate a list of all possible non-final states
	board_nonfinal_states = [board_state for board_state in board_states if not (isWinningBoardState(board_state, 'x') or isWinningBoardState(board_state, 'o'))]

	# Generate a random initial policy
	policy = genRandomPolicy(board_nonfinal_states)

	# Play a game of Noughts and Crosses
	playNoughtsCrosses(policy)