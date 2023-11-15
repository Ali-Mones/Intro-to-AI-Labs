from minimax import minimax, minimax_alphabeta

import pyglet 
import pyglet.window.key as key
import pyglet.window.mouse as mouse
import TreeWindow
from pyglet import shapes

def get_score(cnt):
    return max(0, cnt - 4 + 1)
    

def check_score(board, row, col, player, score):
    row = HEIGHT - 1 - row
    hoz_cnt_left = 0
    hoz_cnt_right = 0
    for i in range(col, WIDTH):
        if board[row][i] == player:
            hoz_cnt_left += 1
        else:
            break
    for i in range(col, -1, -1):
        if board[row][i] == player:
            hoz_cnt_right += 1
        else:
            break
    score -= get_score(hoz_cnt_left - 1)
    score -= get_score(hoz_cnt_right - 1)
    score += get_score(hoz_cnt_left + hoz_cnt_right - 1)
    ver_cnt = 0
    for i in range(row, HEIGHT):
        if board[i][col] == player:
            ver_cnt += 1
        else:
            break
    if ver_cnt >= 4:
        score += 1

    inc_dig_cnt_up = 0
    inc_dig_cnt_down = 0
    for i in range(0, min(row + 1, WIDTH - col)):
        if board[row - i][col + i] == player:
            inc_dig_cnt_up += 1
        else:
            break
    for i in range(0, min(col + 1, HEIGHT - row)):
        if board[row + i][col - i] == player:
            inc_dig_cnt_down += 1
        else:
            break
    score -= get_score(inc_dig_cnt_down - 1)
    score -= get_score(inc_dig_cnt_up - 1)
    score += get_score(inc_dig_cnt_down + inc_dig_cnt_up - 1)
    dec_dig_cnt_up = 0
    dec_dig_cnt_down = 0
    for i in range(0, min(row + 1, col + 1)):
        if board[row - i][col - i] == player:
            dec_dig_cnt_up += 1
        else:
            break
    for i in range(0, min(HEIGHT - row, WIDTH - col)):
        if board[row + i][col + i] == player:
            dec_dig_cnt_down += 1
        else:
            break
    score -= get_score(dec_dig_cnt_down - 1)
    score -= get_score(dec_dig_cnt_up - 1)
    score += get_score(dec_dig_cnt_down + dec_dig_cnt_up - 1)
    return score
    
def apply_move(board, col, column_id, player):
    board[HEIGHT - 1 - column_id[col]][col] = player
    column_id[col] += 1

def get_copy(board):
    c: list[list[int]] = []
    for row in range(HEIGHT):
        c.append([])
        for element in range(WIDTH):
            c[row].append(board[row][element])
    return c


WINDOW_WIDTH, WINDOW_HEIGHT = 950, 600
HEIGHT, WIDTH = 6, 7
START_X, START_Y = 80,0
RADIUS = 31
GAP = 25
START_DRAW_X, START_DRAW_Y = START_X + 28 + RADIUS,START_Y + 28 + RADIUS
PLAYER_ONE = 0
PLAYER_TWO = 1
EMPTY = 2

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, "Connect 4") 
batch = pyglet.graphics.Batch()
game_active = True

board_image = pyglet.image.load('board_image.png')
board_image_rect = pyglet.sprite.Sprite(board_image, x = START_X, y = START_Y)

game_grid: list[list[int]] = [[EMPTY] * WIDTH for j in range(HEIGHT)]
colomn_ind: list[int] = [0] * WIDTH
selected = 6
select_shift = 2 * RADIUS + GAP
x = GAP // 2

score_one = 0
score_two = 0

player = PLAYER_ONE
played = False

label1 = pyglet.text.Label(f"Your Score 0", font_name ='Cooper', font_size = 16, x = 750, y = 560)
label2 = pyglet.text.Label(f"AI Score 0", font_name ='Cooper', font_size = 16, x = 750, y = 520)
# cir = shapes.Circle(START_DRAW_X + 0*GAP + 0 * 2 * RADIUS
#                               , START_DRAW_Y + 0*GAP + 0 * 2 * RADIUS
#                               , RADIUS, 
#                               color = (255,255,0))

btn_rect = [750,200,150,40]
btn_rect_col = (0,255,0)
TreeText = pyglet.text.Label("Show Tree", font_name ='Cooper', font_size = 16, x = btn_rect[0]+20, y = btn_rect[1]+12)
  
def checkCollision(px,py,rx,ry,rw,rh):
    if (px >= rx and px <= rx + rw and py >= ry and py <= ry + rh): return True
    return False

# on draw event 
@window.event 
def on_draw(): 
    global label1,label2,btn_rect_col
    window.clear()
    board_image_rect.draw()
    label1.draw()
    label2.draw()
    shapes.Rectangle(btn_rect[0],btn_rect[1],btn_rect[2],btn_rect[3],color = btn_rect_col).draw()
    TreeText.draw()

    shift_y = 0
    for row in range(HEIGHT-1, -1, -1):
        r = HEIGHT - row - 1
        shift_x = 0
        for col in range(WIDTH):

            c = shapes.Circle(0,0,10)
            if game_grid[row][col] == PLAYER_ONE:
                c = shapes.Circle(START_DRAW_X + shift_x + col * 2 * RADIUS
                              , START_DRAW_Y + shift_y + r * 2 * RADIUS
                              , RADIUS, 
                              color = (255,0,0))
            elif game_grid[row][col] == PLAYER_TWO:
                c = shapes.Circle(START_DRAW_X + shift_x + col * 2 * RADIUS
                              , START_DRAW_Y + shift_y + r * 2 * RADIUS
                              , RADIUS, 
                              color = (255,255,0))
            c.draw()
            shift_x += GAP
        shift_y += GAP
  	
@window.event 
def on_mouse_press(x,y,symbol, modifier): 
    global player,selected,score_one,score_two,label1,label2,played,w,btn_rect_col
    rx,ry,rw,rh = board_image_rect.x,board_image_rect.y,board_image_rect.width,board_image_rect.height
    
    if checkCollision(x,y,rx,ry,rw,rh):            
        selected = (x - GAP // 2) // select_shift - 1
        if selected < 0:
            selected = 0
        elif selected >= WIDTH:
            selected = WIDTH - 1
            
    if((symbol == mouse.RIGHT or symbol == mouse.LEFT) and player == PLAYER_ONE):
        if checkCollision(x,y,rx,ry,rw,rh):
            if colomn_ind[selected] < HEIGHT:
                apply_move(game_grid, selected, colomn_ind, player)
                score_one = check_score(game_grid, colomn_ind[selected] - 1, selected, player, score_one)
                played = False
                player = PLAYER_TWO
                           
                           
    if player == PLAYER_TWO:
        value, move = minimax_alphabeta(get_copy(game_grid), 5, True, colomn_ind)
        apply_move(game_grid, move, colomn_ind, PLAYER_TWO)
        score_two = check_score( game_grid, colomn_ind[move] - 1, move, player, score_two )
        played = True
        player = PLAYER_ONE
        
    label1 = pyglet.text.Label(f"Your Score {score_one}", font_name ='Cooper', font_size = 16, x = 750, y = 560)
    label2 = pyglet.text.Label(f"AI Score {score_two}", font_name ='Cooper', font_size = 16, x = 750, y = 520)
            
    if checkCollision(x,y,*btn_rect):  
        btn_rect_col = (0,0,255)
        hand_cursor = window.get_system_mouse_cursor(window.CURSOR_HAND) 
        window.set_mouse_cursor(hand_cursor)        
        TreeWindow.createWindow()    
        
@window.event 
def on_mouse_release(x,y,symbol, modifier): 
    global btn_rect_col  
    btn_rect_col = (0,255,0) 
    
@window.event 
def on_mouse_motion(x,y,symbol, modifier): 
    global btn_rect_col
    if checkCollision(x,y,*btn_rect):  
        btn_rect_col = (255,0,0)
        hand_cursor = window.get_system_mouse_cursor(window.CURSOR_HAND) 
        window.set_mouse_cursor(hand_cursor) 
    else:
        btn_rect_col = (0,255,0)
        default_cursor = window.get_system_mouse_cursor(window.CURSOR_DEFAULT) 
        window.set_mouse_cursor(default_cursor)
               
              
        
pyglet.clock.schedule_interval(lambda y:y, 1/60) 
# wait_cursor = window.get_system_mouse_cursor(window.CURSOR_HAND) 
# window.set_mouse_cursor(wait_cursor) 
window.set_location(50, 100)
pyglet.app.run() 

# state id ----> (value, move, child id)
tree: dict[int, list[(int, int, int)]]