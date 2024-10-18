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
# +------------------+-------------+---------+-----------+----------+-----------+-----------+
# |      STATE       | DO NOTHING  | UP_KEY  | DOWN_KEY  | LEFT_KEY | RIGHT_KEY |   Q_KEY   |
# +------------------+-------------+---------+-----------+----------+-----------+-----------+
# |      idle        |    idle     | up_anim | down_anim | left_anim| right_anim| quit_game |
# +------------------+-------------+---------+-----------+----------+-----------+-----------+
# |  left_animation  |    idle     | up_anim | down_anim | left_anim| right_anim| quit_game |
# +------------------+-------------+---------+-----------+----------+-----------+-----------+
# | right_animation  |    idle     | up_anim | down_anim | left_anim| right_anim| quit_game |
# +------------------+-------------+---------+-----------+----------+-----------+-----------+
# |  up_animation    |    idle     | up_anim | down_anim | left_anim| right_anim| quit_game |
# +------------------+-------------+---------+-----------+----------+-----------+-----------+
# | down_animation   |    idle     | up_anim | down_anim | left_anim| right_anim| quit_game |
# +------------------+-------------+---------+-----------+----------+-----------+-----------+
# |   quit_game      | quit_game   | quit_game| quit_game| quit_game| quit_game | quit_game |
# +------------------+-------------+---------+-----------+----------+-----------+-----------+



class State(Enum):
    IDLE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    QUIT = 5

class Transition(Enum):
    DO_NOTHING = 0
    UP_KEY = 1
    DOWN_KEY = 2
    LEFT_KEY = 3
    RIGHT_KEY = 4
    Q_KEY = 5

# transition_table[CURRENT STATE][TRANSITION]
transition_table = [
#    DO_NOTHING,   UP_KEY,   DOWN_KEY,   LEFT_KEY,   RIGHT_KEY,      Q_KEY
    [State.IDLE, State.UP, State.DOWN, State.LEFT, State.RIGHT, State.QUIT], # IDLE = 0
    [State.IDLE, State.UP, State.DOWN, State.LEFT, State.RIGHT, State.QUIT], # LEFT = 1
    [State.IDLE, State.UP, State.DOWN, State.LEFT, State.RIGHT, State.QUIT], # RIGHT = 2
    [State.IDLE, State.UP, State.DOWN, State.LEFT, State.RIGHT, State.QUIT], # UP = 3
    [State.IDLE, State.UP, State.DOWN, State.LEFT, State.RIGHT, State.QUIT], # DOWN = 4
    [State.QUIT, State.QUIT, State.QUIT, State.QUIT, State.QUIT, State.QUIT] # QUIT = 5
]



convert_state_to_animation = {
    State.LEFT : left_animation,
    State.RIGHT : right_animation,
    State.UP : up_animation,
    State.DOWN : down_animation,
}

# STATE = ANIMATIONS
# TRANSITION = KEY_PRESS

counter = 1
is_idle = True
animation_state = down_animation
current_state = State.IDLE

running = True

up_key = pygame.Rect(393 - 50,195 - 50, 100, 100)
down_key = pygame.Rect(393 - 50,385 - 50, 100, 100)
left_key = pygame.Rect(176 - 50,399 - 50, 100 , 100)
right_key = pygame.Rect(612 - 50,399 - 50, 100, 100)

transition = Transition.DO_NOTHING


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # GET TRANSITION FOR KEY PRESSES
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                key_press_indicator = down_key

                transition = transition_table[current_state.value][Transition.DOWN_KEY.value]
                
            if event.key == pygame.K_LEFT:
                key_press_indicator = left_key

                transition = transition_table[current_state.value][Transition.LEFT_KEY.value]

                

            if event.key == pygame.K_RIGHT:
                key_press_indicator = right_key
                
                transition = transition_table[current_state.value][Transition.RIGHT_KEY.value]



            if event.key == pygame.K_UP:
                key_press_indicator = up_key

                transition = transition_table[current_state.value][Transition.UP_KEY.value]

            if event.key == pygame.K_q:
                transition = transition_table[current_state.value][Transition.Q_KEY.value]


            if transition != State.QUIT:
                animation_state = convert_state_to_animation[transition]
            
            
                

        # GET TRANSITION FOR DO NOTHING
        if True not in pygame.key.get_pressed():
            transition = transition_table[current_state.value][Transition.DO_NOTHING.value]
        
        current_state = transition


        
                
    
    
    screen.fill((0, 255, 255))

    screen.blit(arrow_keys, (800//2 - arrow_keys.get_width()//2, 600//2 - arrow_keys.get_height()//2))
    


    if current_state == State.IDLE:
        screen.blit(animation_state[0], (800//2 - frame_0.get_width()//2, 600//2 - frame_0.get_height()//2))
    elif current_state == State.QUIT:
        running = False
    else:
        pygame.draw.rect(screen, (255,255,0), key_press_indicator)
        screen.blit(animation_state[counter % 4], (800//2 - frame_0.get_width()//2, 600//2 - frame_0.get_height()//2))
        

    counter += 1
    clock.tick(24)

    print(f"Current State: {current_state}")


    

    pygame.display.flip()

pygame.quit()
sys.exit()