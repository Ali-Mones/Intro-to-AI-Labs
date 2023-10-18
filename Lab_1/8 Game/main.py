import pygame
from sys import exc_info

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('8 Puzzle')
clock = pygame.time.Clock()
game_active = True

start_point = (240, 80)

tile_width = 134
def rects_init():
    sty=0
    sty=start_point[1]
    for i in [1,4,7]:
        stx=start_point[0]
        for j in range(i, i+3):
            if j==9:
                break
            tiles_rects[j]=tiles[j].get_rect(topleft=(stx,sty))
            stx+=tile_width
        sty+=tile_width

def check_select(mouse_pos):
    global selected
    for i in range(1,9):
        if tiles_rects[i].collidepoint(mouse_pos):
            return i
    return -1    

def move_tile(tile):
    global to_tile
    tile_rect = tiles_rects[tile]
    pos = (tile_rect.x-start_point[0])//tile_width+(tile_rect.y-start_point[1])//tile_width*3
    print("pos:",pos)
    if pos%3==0 or pos%3==1:
        if(state[pos+1]=='_'):
            to_tile = (tile_rect.x+tile_width, tile_rect.y)
            state[pos+1]=state[pos]
            state[pos]='_'
            return True
    if pos%3==1 or pos%3==2:
        if(state[pos-1]=='_'):
            to_tile = (tile_rect.x-tile_width, tile_rect.y)
            state[pos-1]=state[pos]
            state[pos]='_'
            return True
    if pos//3==0 or pos//3==1:
        if(state[pos+3]=='_'):
            to_tile = (tile_rect.x, tile_rect.y+tile_width)
            state[pos+3]=state[pos]
            state[pos]='_'
            return True
    if pos//3==1 or pos//3==2:
        if(state[pos-3]=='_'):
            to_tile = (tile_rect.x, tile_rect.y-tile_width)
            state[pos-3]=state[pos]
            state[pos]='_'
            return True
    return False
    
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

play_mode = 1

background = pygame.image.load('Tiles/background2.jpg').convert_alpha()
background = pygame.transform.rotozoom(background, 0, 2)
background_rect = background.get_rect(topleft = (0, 0))

moving = False
selected = 0

state = "12345678_"
state=list(state)
to_tile = 0
from_tile = 0
tile_speed=7
point_cursor = 11
normal_cursor = 0
while game_active:
    mouse = pygame.mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if check_select(mouse.get_pos())!=-1:
            mouse.set_cursor(point_cursor)
        else:
            mouse.set_cursor(normal_cursor)
    screen.blit(background, background_rect)
    if play_mode==1:
        if not moving:
            if mouse.get_pressed()[0]:
                selected=check_select(mouse.get_pos())

                if selected!=-1 and move_tile(selected):
                    moving=True
                    print("moving")
        else:
            tile_rect=tiles_rects[selected]
            if to_tile[0] < tile_rect.x:
                tile_rect.x = max(tile_rect.x-tile_speed,to_tile[0])
            elif to_tile[0] > tile_rect.x:
                tile_rect.x = min(tile_rect.x+tile_speed,to_tile[0])
            elif to_tile[1] < tile_rect.y:
                tile_rect.y = max(tile_rect.y-tile_speed,to_tile[1])
            elif to_tile[1] > tile_rect.y:
                tile_rect.y = min(tile_rect.y+tile_speed,to_tile[1])
            if tile_rect.x==to_tile[0] and tile_rect.y==to_tile[1]:
                moving = False
                print("done")
    elif play_mode==2:
        2
    for i in range(1,9):
        screen.blit(tiles[i],tiles_rects[i])


    # print(mouse.get_pos())
    pygame.display.update()
    clock.tick(60)