import pygame
from enum import Enum
import pygame
import sys

class MODE(Enum):
    IDLE = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP = 4


pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Spritesheet FSM")

sprite_sheet = pygame.image.load("spritesheet.png").convert_alpha()
arrow_keys =  pygame.image.load("arrow_keys.png").convert_alpha()

arrow_keys.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)

key_press_indicator = pygame.Rect(350,100,100,100)

def get_image(frame, width, height, mode):
    mode = mode - 1
    rect = pygame.Rect((frame * width), (mode * height), width, height)
    image = pygame.Surface(rect.size, pygame.SRCALPHA)
    image.blit(sprite_sheet, (0,0), rect)
    return image

frame_0 = get_image(3, 64, 64, MODE.RIGHT.value)

def generate_animation(mode):
    res = []
    for i in range(4):
        res.append(get_image(i, 64, 64, mode))

    return res

clock = pygame.time.Clock()

down_animation = generate_animation(MODE.DOWN.value)
left_animation = generate_animation(MODE.LEFT.value)
right_animation = generate_animation(MODE.RIGHT.value)
up_animation = generate_animation(MODE.UP.value)


# TRANSITION TABLE
#
# +------------------+-------------+---------+-----------+----------+-----------+
# |      STATE       | DO NOTHING  | UP_KEY  | DOWN_KEY  | LEFT_KEY | RIGHT_KEY |
# +------------------+-------------+---------+-----------+----------+-----------+
# |      idle        |    idle     | up_anim | down_anim | left_anim| right_anim|
# +------------------+-------------+---------+-----------+----------+-----------+
# |  left_animation  |    idle     | up_anim | down_anim | left_anim| right_anim|
# +------------------+-------------+---------+-----------+----------+-----------+
# | right_animation  |    idle     | up_anim | down_anim | left_anim| right_anim|
# +------------------+-------------+---------+-----------+----------+-----------+
# |  up_animation    |    idle     | up_anim | down_anim | left_anim| right_anim|
# +------------------+-------------+---------+-----------+----------+-----------+
# | down_animation   |    idle     | up_anim | down_anim | left_anim| right_anim|
# +------------------+-------------+---------+-----------+----------+-----------+


#SIMPLIFIED TRANSITION TABLE

transition_table = {
    pygame.K_LEFT : left_animation,
    pygame.K_RIGHT : right_animation,
    pygame.K_UP: up_animation,
    pygame.K_DOWN : down_animation,
}

# STATE = ANIMATIONS
# TRANSITION = KEY_PRESS

counter = 1
is_idle = True
current_state = down_animation
running = True

up_key = pygame.Rect(393 - 50,195 - 50, 100, 100)
down_key = pygame.Rect(393 - 50,385 - 50, 100, 100)
left_key = pygame.Rect(176 - 50,399 - 50, 100 , 100)
right_key = pygame.Rect(612 - 50,399 - 50, 100, 100)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # GET TRANSITION FOR KEY PRESSES
        if event.type == pygame.KEYDOWN:
            is_idle = False
            if event.key == pygame.K_DOWN:
                key_press_indicator = down_key
                current_state = transition_table[pygame.K_DOWN]
            if event.key == pygame.K_LEFT:
                key_press_indicator = left_key
                current_state = transition_table[pygame.K_LEFT]
            if event.key == pygame.K_RIGHT:
                key_press_indicator = right_key
                current_state = transition_table[pygame.K_RIGHT]
            if event.key == pygame.K_UP:
                key_press_indicator = up_key
                current_state = transition_table[pygame.K_UP]

        # GET TRANSITION FOR DO NOTHING
        if True not in pygame.key.get_pressed():
            is_idle = True
                
    
    
    screen.fill((0, 255, 255))

    screen.blit(arrow_keys, (800//2 - arrow_keys.get_width()//2, 600//2 - arrow_keys.get_height()//2))
    


    if is_idle:
        screen.blit(current_state[0], (800//2 - frame_0.get_width()//2, 600//2 - frame_0.get_height()//2))
    else:
        pygame.draw.rect(screen, (255,255,0), key_press_indicator)
        screen.blit(current_state[counter % 4], (800//2 - frame_0.get_width()//2, 600//2 - frame_0.get_height()//2))
        

    counter += 1
    clock.tick(5)


    

    pygame.display.flip()

pygame.quit()
sys.exit()