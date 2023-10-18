import pygame
from sys import exit




pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('8 Puzzle')
clock = pygame.time.Clock()
game_active = True

START_POINT = (240, 80)

TILE_WIDTH = 134
def rects_init():
    sty=0
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

text_font=pygame.font.Font('Font/Pixeltype.ttf',40)
# 1: play game, 2: setup board
play_mode = 2

background = pygame.image.load('Tiles/background2.jpg').convert_alpha()
background = pygame.transform.rotozoom(background, 0, 2)
background_rect = background.get_rect(topleft = (0, 0))

moving = False
selected = 0

state = "_________"
state=list(state)


to_tile = (0,0)
from_tile = 0
TILE_SPEED=7
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

while game_active:
    mouse = pygame.mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if check_select(mouse.get_pos())!=-1:
            mouse.set_cursor(POINT_CURSOR)
        else:
            mouse.set_cursor(NORMAL_CURSOR)
    screen.blit(background, background_rect)

    # playing
    if play_mode==1:
        if not moving:
            if mouse.get_pressed()[0]:
                selected=check_select(mouse.get_pos())

                if selected!=-1 and check_move(selected):
                    moving=True
                    print("moving")
        else:
            move_tile()
    # start screen 
    elif play_mode==2:
        mouse_pos=mouse.get_pos()
        screen.blit(start_button,start_button_rect)
        if moving:
            move_tile()
        elif not mouse_hold:
            if mouse.get_pressed()[0]:
                if start_button_rect.collidepoint(mouse_pos):
                    set_state()
                    print(state)
                    play_mode=1
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