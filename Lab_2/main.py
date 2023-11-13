import pygame
from minimax import minimax
def check_score(board, row, col, player, score):
    row = HEIGHT - 1 - row
    hoz_cnt_left = 0
    hoz_cnt_right = 0
    for i in range(col, WIDTH):
        if board[row][i]==player: hoz_cnt_left+=1
        else: break
    for i in range(col-1, -1, -1):
        if board[row][i]==player: hoz_cnt_right+=1
        else: break
    if hoz_cnt_left <= 4 and hoz_cnt_right < 4:
        if hoz_cnt_right + hoz_cnt_left >= 4:
            score+=1

    ver_cnt = 0
    for i in range(row, HEIGHT):
        if board[i][col]==player: ver_cnt+=1
        else: break
    if ver_cnt==4:
        score += 1
    inc_dig_cnt_up = 0
    inc_dig_cnt_down = 0
    for i in range(0, min(row+1, WIDTH-col)):
        if board[row-i][col+i]==player: inc_dig_cnt_up+=1
        else: break
    for i in range(1, min(col+1, HEIGHT-row)):
        if board[row+i][col-i]==player: inc_dig_cnt_down+=1
        else: break
    if inc_dig_cnt_down < 4 and inc_dig_cnt_up <= 4:
        if inc_dig_cnt_up + inc_dig_cnt_down >= 4:
            score+=1
    dec_dig_cnt_up = 0
    dec_dig_cnt_down = 0
    for i in range(0, min(row+1, col+1)):
        if board[row-i][col-i]==player: dec_dig_cnt_up+=1
        else: break
    for i in range(1, min(HEIGHT-row, WIDTH-col)):
        if board[row+i][col+i]==player: dec_dig_cnt_down+=1
        else: 
            break
    if dec_dig_cnt_down < 4 and dec_dig_cnt_up <= 4:
        if dec_dig_cnt_up + dec_dig_cnt_down >= 4:
            score+=1
    return score

def apply_move(board, col, column_id, player):
    board[HEIGHT-1-column_id[col]][col] = player
    column_id[col] += 1
def get_copy(board):
	c: list[list[int]]=[]
	for row in range(HEIGHT):
		c.append([])
		for element in range(WIDTH):
			c[row].append(board[row][element])
	return c

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
HEIGHT, WIDTH = 6, 7
START_X, START_Y = 80, 50
RADIUS = 31
GAP = 25
START_DRAW_X, START_DRAW_Y = START_X+28+RADIUS, 80+RADIUS
PLAYER_ONE = 0
PLAYER_TWO = 1
EMPTY = 2
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
clock = pygame.time.Clock()
game_acive = True
board_image = pygame.image.load("board_image.png").convert_alpha()
board_image_rect = board_image.get_rect(topleft=(START_X, START_Y))

game_grid: list[list[int]] = [[EMPTY]*WIDTH for j in range(HEIGHT)]
colomn_ind: list[int] = [0]*WIDTH
selected = 6
select_shift = 2*RADIUS+GAP
# print(game_grid)
# print("here", colomn_ind)
x = GAP//2

score_one = 0
score_two = 0

text_font = pygame.font.Font('font/regular_font.otf', 40)

column_rects:list[pygame.Rect] = []
for i in range(WIDTH):
    column_rects.append(pygame.Rect(START_X+x, START_Y, select_shift, board_image_rect.height))
    x+= select_shift

player = PLAYER_ONE
played = False
while game_acive:
    
    mouse = pygame.mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if player == PLAYER_ONE and event.type == pygame.MOUSEBUTTONDOWN:
            if board_image_rect.collidepoint(mouse.get_pos()):
                if colomn_ind[selected] < HEIGHT:
                    apply_move(game_grid, selected, colomn_ind, player)
                    score_one = check_score(game_grid, colomn_ind[selected]-1, selected, player,score_one)
                    played=True
                    

    screen.fill("Black")
    screen.blit(board_image, board_image_rect)
    shift_y = GAP*(HEIGHT-1)
    for row in range(HEIGHT-1,-1, -1):
        shift_x = 0
        for col in range(WIDTH):
            # print(row, col)
            if game_grid[row][col] == PLAYER_ONE:
                pygame.draw.circle(screen, "Red", (START_DRAW_X + shift_x + col * 2 * RADIUS, START_DRAW_Y + shift_y + row * 2 * RADIUS), RADIUS, 0)
            elif game_grid[row][col] == PLAYER_TWO:
                pygame.draw.circle(screen, "Yellow", (START_DRAW_X + shift_x + col * 2 * RADIUS, START_DRAW_Y + shift_y + row * 2 * RADIUS), RADIUS, 0)
            shift_x += GAP
        shift_y -= GAP

    score1 = text_font.render(f"Your Score {score_one}", False, "White")
    score2 = text_font.render(f"AI Score {score_two}", False, "White")
    screen.blit(score1, score1.get_rect(topright = (950, 20)))
    screen.blit(score2, score2.get_rect(topright = (950, 60)))

    if player==PLAYER_TWO:
        print(game_grid)
        value, move = minimax(get_copy(game_grid), 5, True, colomn_ind)
        print(value, move)
        apply_move(game_grid, move, colomn_ind, PLAYER_TWO)
        score_two = check_score(game_grid, colomn_ind[move]-1, move, player,score_two)
        player = PLAYER_ONE
    if played:
         played = False
         player = PLAYER_TWO
    if board_image_rect.collidepoint(mouse.get_pos()):
        selected = (mouse.get_pos()[0]-GAP//2)//select_shift-1
        if selected<0: selected=0
        elif selected>=WIDTH: selected=WIDTH-1
        # print(selected)
        mouse.set_cursor(11)
    else:
        mouse.set_cursor(0)
    # for i in range(len(column_rects)):
    #     if (mouse.get_pos())




    # Draw the arrow
    if player==PLAYER_ONE:
        pygame.draw.polygon(screen, "Red", [(START_DRAW_X-RADIUS + selected*select_shift,START_Y-40), (START_DRAW_X-RADIUS+2*RADIUS+selected*select_shift, START_Y-40), (START_DRAW_X-RADIUS+RADIUS+selected*select_shift, START_Y)])
    else:
        pygame.draw.polygon(screen, "Yellow", [(START_DRAW_X-RADIUS + selected*select_shift,START_Y-40), (START_DRAW_X-RADIUS+2*RADIUS+selected*select_shift, START_Y-40), (START_DRAW_X-RADIUS+RADIUS+selected*select_shift, START_Y)])
    
    # print(mouse.get_pos())
    # pygame.draw.circle(screen, "Yellow", (100,100), 100)    
    pygame.display.update()
    clock.tick(60)

