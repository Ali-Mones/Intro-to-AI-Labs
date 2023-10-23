import pygame, time
from sys import exit

import ai_algorithms

# state = "12345678_"
# parents = ai_algorithms.BFS(state)
# sol = "_12345678"
# print(sol)
# while parents[sol] != sol:
#     sol = parents[sol]
#     print(sol)




pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('8 Puzzle')
clock = pygame.time.Clock()
game_active = True

START_POINT = (240, 80)
PLAY_GAME = 2
SET_UP_BOARD = 1
TILE_WIDTH = 134
def rects_init():
    sty=START_POINT[1]
    for i in [1,4,7]:
        stx=START_POINT[0]
        for j in range(i, i+3):
            if j==9:
                break
            tiles_rects[j]=tiles[j].get_rect(topleft=(stx,sty))
            stx+=TILE_WIDTH
        sty+=TILE_WIDTH

def check_select(mouse_pos, ignore_tile=-1):
    for i in range(1,9):
        if i!=ignore_tile and tiles_rects[i].collidepoint(mouse_pos):
            return i
    return -1    

def check_move(tile):
    global to_tile
    tile_rect = tiles_rects[tile]
    pos = (tile_rect.x-START_POINT[0])//TILE_WIDTH+(tile_rect.y-START_POINT[1])//TILE_WIDTH*3
    print("pos:",pos)
    if pos%3==0 or pos%3==1:
        if(state[pos+1]=='_'):
            to_tile = (tile_rect.x+TILE_WIDTH, tile_rect.y)
            state[pos+1]=state[pos]
            state[pos]='_'
            return True
    if pos%3==1 or pos%3==2:
        if(state[pos-1]=='_'):
            to_tile = (tile_rect.x-TILE_WIDTH, tile_rect.y)
            state[pos-1]=state[pos]
            state[pos]='_'
            return True
    if pos//3==0 or pos//3==1:
        if(state[pos+3]=='_'):
            to_tile = (tile_rect.x, tile_rect.y+TILE_WIDTH)
            state[pos+3]=state[pos]
            state[pos]='_'
            return True
    if pos//3==1 or pos//3==2:
        if(state[pos-3]=='_'):
            to_tile = (tile_rect.x, tile_rect.y-TILE_WIDTH)
            state[pos-3]=state[pos]
            state[pos]='_'
            return True
    return False

def move_tile():
    global moving
    tile_rect=tiles_rects[selected]
    if to_tile[0] < tile_rect.x:
        tile_rect.x = max(tile_rect.x-TILE_SPEED,to_tile[0])
    elif to_tile[0] > tile_rect.x:
        tile_rect.x = min(tile_rect.x+TILE_SPEED,to_tile[0])
    elif to_tile[1] < tile_rect.y:
        tile_rect.y = max(tile_rect.y-TILE_SPEED,to_tile[1])
    elif to_tile[1] > tile_rect.y:
        tile_rect.y = min(tile_rect.y+TILE_SPEED,to_tile[1])
    if tile_rect.x==to_tile[0] and tile_rect.y==to_tile[1]:
        moving = False
        print("done")

def set_state():
    for i in range(1,9):
        tile_rect_pos = (tiles_rects[i].x-START_POINT[0])//TILE_WIDTH+(tiles_rects[i].y-START_POINT[1])//TILE_WIDTH*3 
        print(i,tile_rect_pos)
        state[tile_rect_pos]=f"{i}"
    
def auto_animation(prev=False):
    if not solved_moves_list:
        return
    global solved_moves_cnt, to_tile, state, selected, moving
    cur_state = solved_moves_list[solved_moves_cnt]
    # print(solved_moves_list)
    if prev:
        if solved_moves_cnt==0:
            print("Here1")
            return
        for i in range(9):
            if cur_state[i]=='_':
                solved_moves_cnt-=1
                state = list(solved_moves_list[solved_moves_cnt])
                selected = int(state[i])
                to_tile=(START_POINT[0]+TILE_WIDTH*(i%3),START_POINT[1]+TILE_WIDTH*(i//3))
                moving = True
                return
    else:
        if solved_moves_cnt >= len(solved_moves_list)-1:
            print("Here1")
            return
        for i in range(9):
            if cur_state[i]=='_':
                solved_moves_cnt+=1
                state = list(solved_moves_list[solved_moves_cnt])
                selected = int(state[i])
                to_tile=(START_POINT[0]+TILE_WIDTH*(i%3),START_POINT[1]+TILE_WIDTH*(i//3))
                moving = True
                print("WOrkes")
                return


def move_tile_animation():
    # get child
    global solved_moves_cnt, to_tile, state
    cur_state = solved_moves_list[solved_moves_cnt]
    print(cur_state)
    if solved_moves_cnt >= len(solved_moves_list)-1:
        return -1
    solved_moves_cnt+=1
    for i in range(9):
        if cur_state[i]=='_':
            state = list(solved_moves_list[solved_moves_cnt])
            tile_to_move = int(state[i])
            to_tile=(START_POINT[0]+TILE_WIDTH*(i%3),START_POINT[1]+TILE_WIDTH*(i//3))
            
            return tile_to_move


def jumb_to_final():
    global solved_moves_cnt, state
    solved_moves_cnt = len(solved_moves_list) - 1
    cur_state = solved_moves_list[solved_moves_cnt]
    state = list(cur_state)
    sty=START_POINT[1]
    stx=START_POINT[0]
    xstep = 0 
    ystep = 0
    for ch in cur_state:
        if ch != "_":
            el = int(ch)
            tiles_rects[el].topleft = (stx+xstep*TILE_WIDTH,sty+ystep*TILE_WIDTH)
        xstep+=1
        if xstep == 3:
            xstep = 0
            ystep+=1
        

tiles = {
    1: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_01_134.png').convert_alpha(),
    2: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_02_134.png').convert_alpha(),
    3: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_03_134.png').convert_alpha(),
    4: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_04_134.png').convert_alpha(),
    5: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_05_134.png').convert_alpha(),
    6: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_06_134.png').convert_alpha(),
    7: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_07_134.png').convert_alpha(),
    8: pygame.image.load('Tiles/tile1_number_134_pixels/tile1_08_134.png').convert_alpha(),
}
tiles_rects:dict[int, pygame.Rect] = {}
rects_init()

text_font=pygame.font.Font('Font/pixeltype.ttf',50)

solve_dfs_text = text_font.render("SOLVE DFS",False,"White")
solve_dfs_text_rect = solve_dfs_text.get_rect(topleft = (30, 50))

solve_bfs_text = text_font.render("SOLVE BFS",False,"White")
solve_bfs_text_rect = solve_bfs_text.get_rect(topleft = (30, 120))

solve_manhattan_text = text_font.render("A* Manhattan",False,"White")
solve_manhattan_text_rect = solve_manhattan_text.get_rect(topleft = (30, 190))

solve_euc_text = text_font.render("A* Euclidean",False,"White")
solve_euc_text_rect = solve_euc_text.get_rect(topleft = (30, 260))

show_text = text_font.render("Show Moves",False,"White")
show_text_rect = show_text.get_rect(topleft = (30, 330))

next_text = text_font.render("Next",False,"White")
next_text_rect = next_text.get_rect(topleft = (30, 400))

prev_text = text_font.render("Prev",False,"White")
prev_text_rect = prev_text.get_rect(topleft = (30, 470))

jumb_text = text_font.render("Jumb to end",False,"White")
jumb_text_rect = jumb_text.get_rect(topleft = (30, 540))


path_cost_text = text_font.render("Path Cost:",False,"Green")
path_cost_text_rect = path_cost_text.get_rect(topleft = (700, 50))

nodes_text = text_font.render("Nodes Expanded:",False,"Green")
nodes_text_rect = nodes_text.get_rect(topleft = (700, 150))

depth_text = text_font.render("Search Depth:",False,"Green")
depth_text_rect = depth_text.get_rect(topleft = (700, 250))

time_text = text_font.render("Time:",False,"Green")
time_text_rect = time_text.get_rect(topleft = (700, 350))

unsolvable_text = text_font.render("Unsolvable:'(",False,"Blue")
unsolvable_text_rect = unsolvable_text.get_rect(topleft = (700, 450))



# 1: play game, 2: setup board
play_mode = SET_UP_BOARD

background = pygame.image.load('Tiles/background2.jpg').convert_alpha()
background = pygame.transform.rotozoom(background, 0, 2)
background_rect = background.get_rect(topleft = (0, 0))

moving = False
selected = 0

state = "_________"
state=list(state)

depth = 0
time_spent = 0
nodes_expanded = 0
path_cost = 0

to_tile = (0,0)
from_tile = 0
TILE_SPEED=11
POINT_CURSOR = 11
NORMAL_CURSOR = 0

# attributes for start of game
mouse_hold = False
mouse_hold_x=0
mouse_hold_y=0
mouse_hold_original_pos = (0,0)
held_tile=0
held_tile_rect=None
# start button
start_button = pygame.image.load('Tiles/play.png').convert_alpha()
start_button = pygame.transform.rotozoom(start_button,0,0.4)
start_button_rect = start_button.get_rect(topleft=(30,50))

show_solved_moves_animation = False
solved_moves_list:list[str] = []
solved_moves_cnt:int=0
mouse_down = False
ready_to_animate = False

unsolvable = False



while game_active:
    mouse = pygame.mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Donw")
            mouse_down=True
        elif event.type==pygame.MOUSEBUTTONUP:
            print("Up")
            mouse_down=False
        
        
    if check_select(mouse.get_pos())!=-1:
        mouse.set_cursor(POINT_CURSOR)
    else:
        mouse.set_cursor(NORMAL_CURSOR)
    screen.blit(background, background_rect)

    # playing
    if play_mode==PLAY_GAME:
        
        if moving:
            move_tile()
        elif show_solved_moves_animation:
            if moving:
                move_tile()
            else:
                selected = move_tile_animation()
                moving = True
                print("moving ", to_tile)
                print("moving tile ", selected)
                if selected == -1:
                    # solved_moves_list.clear()
                    show_solved_moves_animation = False
                    moving = False
        elif mouse_down:
            mouse_down=False
            
            #left BK
            pygame.draw.rect(background,(0,0,76), (10, 10, 227, 580))
            pygame.draw.rect(background, pygame.Color("black"), (10, 10, 227, 580), width=5)
            
            #right BK
            pygame.draw.rect(background,(0,0,76), (690 , 10, 280, 580))
            pygame.draw.rect(background, pygame.Color("black"), (690, 10, 280, 580), width=5)
            
            screen.blit(solve_bfs_text, solve_bfs_text_rect)
            screen.blit(solve_dfs_text, solve_bfs_text_rect)
            screen.blit(solve_manhattan_text, solve_manhattan_text_rect)
            screen.blit(solve_euc_text, solve_euc_text_rect)
            screen.blit(show_text, show_text_rect)
            screen.blit(next_text, next_text_rect)
            screen.blit(prev_text, prev_text_rect)
            
            screen.blit(path_cost_text, path_cost_text_rect)
            screen.blit(text_font.render(f"{path_cost}", False, "Yellow"), (700, 100))

            screen.blit(nodes_text, nodes_text_rect)
            screen.blit(text_font.render(f"{nodes_expanded}", False, "Yellow"), (700, 200))

            screen.blit(depth_text, depth_text_rect)
            screen.blit(text_font.render(f"{depth}", False, "Yellow"), (700, 300))

            screen.blit(time_text, time_text_rect)
            screen.blit(text_font.render(f"{time_spent} ms", False, "Yellow"), (700, 400))

            screen.blit(jumb_text, jumb_text_rect)

            if unsolvable:
                screen.blit(unsolvable_text, unsolvable_text_rect)
                
            mouse_pos = mouse.get_pos()
            parents = []
            start = time.time()
            
            if solve_bfs_text_rect.collidepoint(mouse_pos):
                parents = ai_algorithms.BFS("".join(state))
            elif solve_dfs_text_rect.collidepoint(mouse_pos):
                parents = ai_algorithms.DFS("".join(state))
            elif solve_manhattan_text_rect.collidepoint(mouse_pos):
                parents = ai_algorithms.AStarManhattan("".join(state))
            elif solve_euc_text_rect.collidepoint(mouse_pos):
                parents = ai_algorithms.AStarEuclidean("".join(state))
            end = time.time()
            
            if next_text_rect.collidepoint(mouse_pos):
                auto_animation(False)
            elif prev_text_rect.collidepoint(mouse_pos):
                auto_animation(True)
                
            if parents == None:
                print("Not solvable")
                unsolvable=True
                solved_moves_list = []
                nodes_expanded = ai_algorithms.nodes_expanded
                depth = ai_algorithms.depth
                time_spent = round((end - start)*1000, 5)
                path_cost = 0
            elif len(parents)!=0:
                # print("Parents",parents)
                unsolvable=False
                nodes_expanded = ai_algorithms.nodes_expanded
                depth = ai_algorithms.depth
                time_spent = round((end - start)*1000, 5)
                sol = "_12345678"
                solved_moves_list.clear()
                solved_moves_list.append(sol)
                while parents[sol] != sol:
                    sol = parents[sol]
                    solved_moves_list.append(sol)
                ready_to_animate= len(solved_moves_list)>0
                solved_moves_cnt=0
                path_cost = len(solved_moves_list) - 1
                print("Depth:", ai_algorithms.nodes_expanded)
                solved_moves_list.reverse()
                print(len(solved_moves_list))
            elif show_text_rect.collidepoint(mouse_pos):
                if ready_to_animate and solved_moves_cnt < len(solved_moves_list) - 1:
                    print("start animation")
                    print(solved_moves_list)
                    show_solved_moves_animation=True
            elif jumb_text_rect.collidepoint(mouse_pos):
                if ready_to_animate:
                    jumb_to_final()
                ready_to_animate = False

        else:
            #left BK
            pygame.draw.rect(background,(0,0,76), (10, 10, 227, 580))
            pygame.draw.rect(background, pygame.Color("black"), (10, 10, 227, 580), width=5)
            
            #right BK
            pygame.draw.rect(background,(0,0,76), (690 , 10, 280, 580))
            pygame.draw.rect(background, pygame.Color("black"), (690, 10, 280, 580), width=5)
            
            screen.blit(solve_bfs_text, solve_bfs_text_rect)
            screen.blit(solve_dfs_text, solve_dfs_text_rect)
            screen.blit(solve_manhattan_text, solve_manhattan_text_rect)
            screen.blit(solve_euc_text, solve_euc_text_rect)
            screen.blit(show_text, show_text_rect)
            screen.blit(next_text, next_text_rect)
            screen.blit(prev_text, prev_text_rect)

            screen.blit(path_cost_text, path_cost_text_rect)
            screen.blit(text_font.render(f"{path_cost}", False, "Yellow"), (700, 100))

            screen.blit(nodes_text, nodes_text_rect)
            screen.blit(text_font.render(f"{nodes_expanded}", False, "Yellow"), (700, 200))

            screen.blit(depth_text, depth_text_rect)
            screen.blit(text_font.render(f"{depth}", False, "Yellow"), (700, 300))

            screen.blit(time_text, time_text_rect)
            screen.blit(text_font.render(f"{time_spent} ms", False, "Yellow"), (700, 400))

            screen.blit(jumb_text, jumb_text_rect)

            if unsolvable:
                screen.blit(unsolvable_text, unsolvable_text_rect)
            if mouse.get_pressed()[0]:
                selected=check_select(mouse.get_pos())
                print("8**************",selected)
                if selected!=-1 and check_move(selected):
                    moving=True
                    ready_to_animate=False
                    solved_moves_list=[]
                    print("STTATATATAT")
    # start screen 
    elif play_mode==SET_UP_BOARD:
        mouse_pos=mouse.get_pos()
        screen.blit(start_button,start_button_rect)
        if moving:
            move_tile()
        elif not mouse_hold:
            if mouse_down:
                mouse_down=False
                if start_button_rect.collidepoint(mouse_pos):
                    set_state()
                    print(state)
                    play_mode=PLAY_GAME
                else:
                    held_tile = check_select(mouse_pos)
                    if held_tile != -1:
                        mouse_hold=True
                        held_tile_rect=tiles_rects[held_tile]
                        mouse_hold_original_pos=held_tile_rect.topleft
                        mouse_hold_x=mouse_pos[0]-(held_tile_rect.x)
                        mouse_hold_y=mouse_pos[1]-(held_tile_rect.y)
        else:
            if mouse.get_pressed()[0]:
                held_tile_rect.x=mouse_pos[0]-mouse_hold_x
                held_tile_rect.y=mouse_pos[1]-mouse_hold_y
            else:
                mouse_hold=False
                selected=check_select(mouse_pos,held_tile)
                if selected!=-1:
                    held_tile_rect.x=(mouse_pos[0]-START_POINT[0])//TILE_WIDTH*TILE_WIDTH+START_POINT[0]
                    held_tile_rect.y=(mouse_pos[1]-START_POINT[1])//TILE_WIDTH*TILE_WIDTH+START_POINT[1]
                    to_tile=mouse_hold_original_pos
                    moving=True
                else:
                    # check for empty space
                    if mouse_pos[0]>=START_POINT[0] and mouse_pos[0]<=START_POINT[0]+3*TILE_WIDTH\
                    and mouse_pos[1]>=START_POINT[1] and mouse_pos[1]<=START_POINT[1]+3*TILE_WIDTH\
                    :
                        moving=True
                        selected=held_tile
                        to_tile=((mouse_pos[0]-START_POINT[0])//TILE_WIDTH*TILE_WIDTH+START_POINT[0],
                                 (mouse_pos[1]-START_POINT[1])//TILE_WIDTH*TILE_WIDTH+START_POINT[1])
                    else:
                        held_tile_rect.topleft=mouse_hold_original_pos

    for i in range(1,9):
        screen.blit(tiles[i],tiles_rects[i])


    # print(mouse.get_pos())
    pygame.display.update()
    clock.tick(60)
