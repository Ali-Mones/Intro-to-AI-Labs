import math
HUMAN = 0
AI = 1
EMPTY = 2
HEIGHT, WIDTH = 6, 7
def detect_winner(board):
	for c in range(WIDTH-3):
		for r in range(HEIGHT):
			if board[r][c] != EMPTY and board[r][c] == board[r][c+1] and board[r][c] == board[r][c+2] and board[r][c] == board[r][c+3]:
				return board[r][c]

	for c in range(WIDTH):
		for r in range(HEIGHT-3):
			if board[r][c] != EMPTY and board[r][c] == board[r+1][c] and board[r][c] == board[r+2][c] and board[r][c] == board[r+3][c]:
				return board[r][c]

	for c in range(WIDTH-3):
		for r in range(HEIGHT-3):
			if board[r][c] != EMPTY and board[r][c] == board[r+1][c+1] and board[r][c] == board[r+2][c+2] and board[r][c] == board[r+3][c+3]:
				return board[r][c]

	# Check negatively sloped diaganols
	for c in range(WIDTH-3):
		for r in range(3, HEIGHT):
			if board[r][c] != EMPTY and board[r][c] == board[r-1][c+1] and board[r][c] == board[r-2][c+2] and board[r][c] == board[r-3][c+3]:
				return board[r][c]
	return EMPTY

def evaluate_group(group):
	ai_cnt = 0
	human_cnt = 0
	empty_cnt = 0
	for g in group:
		if g==AI:ai_cnt+=1
		elif g==HUMAN: human_cnt+=1
		else: empty_cnt+=1
	if ai_cnt > 0 and human_cnt > 0:
		# no one can win
		return 0
	if ai_cnt > 0:
		if ai_cnt == 1:
			return 1
		if ai_cnt == 2:
			return 4
		if ai_cnt == 3:
			return 10
		if ai_cnt == 4:
			return 80
	if human_cnt == 1:
		return -1
	if human_cnt == 2:
		return -4
	if human_cnt == 3:
		return -10
	if human_cnt == 4:
		return -80
	return 0


def hueristic(board):
	score = 0
	# horizontal
	for c in range(WIDTH-3):
		for r in range(HEIGHT):
			group = [board[r][c],board[r][c+1],board[r][c+2],board[r][c+3]]
			score += evaluate_group(group)

	for c in range(WIDTH):
		for r in range(HEIGHT-3):
			group = [board[r][c],board[r+1][c],board[r+2][c],board[r+3][c]]
			score += evaluate_group(group)

	for c in range(WIDTH-3):
		for r in range(HEIGHT-3):
			group = [board[r][c],board[r+1][c+1],board[r+2][c+2],board[r+3][c+3]]
			score+= evaluate_group(group)

	# Check negatively sloped diaganols
	for c in range(WIDTH-3):
		for r in range(3, HEIGHT):
			group = [board[r][c],board[r-1][c+1],board[r-2][c+2],board[r-3][c+3]]
			score+= evaluate_group(group)
	return score
# return best value of childern along with the best move

def parr(board):
	for row in board:
		print(row)

def get_copy(board):
	c: list[list[int]]=[]
	for row in range(HEIGHT):
		c.append([])
		for element in range(WIDTH):
			c[row].append(board[row][element])
	return c


def minimax(board: list[list[int]], depth: int, maximizing: bool, colomn_ind: list[int]) -> (int, int):
	columns = [int(i) for i in range(len(colomn_ind)) if colomn_ind[i] < HEIGHT]
	# print("array: ")
	# parr(board)
	# print("column_ind:")
	# print(colomn_ind)
	# print("columns:")
	# print(columns)
	if not columns:
		print(colomn_ind)
		winner = detect_winner(board)
		# print("winner:", winner)
		if winner==AI:
			return (math.inf, -1)
		elif winner == HUMAN:
			return (-math.inf, -1)
		else:
			return(0, -1)
		
	if depth == 0:
		# print("depth ended")
		score = hueristic(board)
		# parr(board)
		return (score, -1)
	
	if maximizing:
		# print(maximizing)
		value = -math.inf       
		move = columns[0]
		for col in columns:
			new_board = get_copy(board)
			new_colomn_ind = colomn_ind.copy()

			new_board[HEIGHT-1-colomn_ind[col]][col] = AI
			new_colomn_ind[col]+=1

			new_value, new_move = minimax(new_board, depth-1, False, new_colomn_ind)
			if new_value>value:
				value=new_value
				move=col
		return value, move
	else:
		# print(maximizing)
		value = math.inf   
		move = columns[0]    
		for col in columns:
			new_board = get_copy(board)
			new_colomn_ind = colomn_ind.copy()

			new_board[HEIGHT-1-colomn_ind[col]][col] = HUMAN
			new_colomn_ind[col]+=1

			new_value, new_move = minimax(new_board, depth-1, True, new_colomn_ind)
			if new_value<value:
				value=new_value
				move=col
		return value, move
	

# game_grid: list[list[int]] = [[EMPTY]*WIDTH for j in range(HEIGHT)]
# game_grid[HEIGHT-1][2] = HUMAN
# column_ind = [0,0,1,0,0,0,0]
# parr((game_grid))
# c = get_copy(game_grid)
# c[0][0] =10000
# print(game_grid)
# print(c)
# print(c==game_grid)

# parr(game_grid)
# print(minimax(get_copy(game_grid), 2, True, column_ind))
# parr(game_grid)
# print(column_ind)
