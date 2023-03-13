import pygame as p  
import os
from klasy import character


WIDTH, HEIGHT = 1280,600
WIN = p.display.set_mode((WIDTH,HEIGHT)) 
p.display.set_caption("STAR WARS: A NEW HOPE (fan version)")

WHITE = (255,255,255)

FPS = 60

LUKE_WIDTH, LUKE_HEIGHT = 180, 210
BEN_WIDTH, BEN_HEIGHT = 112, 217

VEL = 5

Y_GRAVITY = 1

JUMP_HEIGHT = 20

Y_VELOCITY = JUMP_HEIGHT

jumping = False

LUKE_SKYWALKER_IMAGE = p.image.load(os.path.join('postacie','luke_skywalker1.png'))
LUKE_SKYWALKER_ATTACKING_IMAGE = p.image.load(os.path.join('postacie','luke_skywalker_attacking.png'))
JUMPING_LUKE_SKYWALKER_IMAGE = p.image.load(os.path.join('postacie','luke_jumping1.png'))

BEN_KENOBI_IMAGE = p.image.load(os.path.join('postacie','ben_kenobi.png'))
JUMPING_BEN_KENOBI_IMAGE = p.image.load(os.path.join('postacie','ben_kenobi_jumping.png'))

LEIA_ORGANA = p.image.load(os.path.join('postacie','leia_organa.png'))

DARTH_VADER = p.image.load(os.path.join('postacie','darth_vader.png'))

TATOOINE_IMAGE = p.image.load(os.path.join('miejsca','tatoine.jpg'))

LUKE = character(LUKE_WIDTH,LUKE_HEIGHT,LUKE_SKYWALKER_IMAGE,LUKE_SKYWALKER_ATTACKING_IMAGE,
                 JUMPING_LUKE_SKYWALKER_IMAGE,VEL,)

# BEN_KENOBI = character(BEN_WIDTH, BEN_HEIGHT, BEN_KENOBI_IMAGE, BE)

def draw_ben(ben,direction,ben_jumping):
    if ben_jumping == True: 
        if direction == "right":
            WIN.blit(JUMPING_BEN_KENOBI_IMAGE,(ben.x,ben.y))
        if direction == "left":
            character_left_flipped = p.transform.flip(JUMPING_BEN_KENOBI_IMAGE, True, False)
            WIN.blit(character_left_flipped, (ben.x-119, ben.y))
    else:
        if direction == "right":
            WIN.blit(BEN_KENOBI_IMAGE,(ben.x,ben.y))
        if direction == "left":
            character_left_flipped = p.transform.flip(BEN_KENOBI_IMAGE, True, False)
            WIN.blit(character_left_flipped, (ben.x, ben.y))

def draw_window(ben_direction,ben,ben_jumping):
    WIN.blit(TATOOINE_IMAGE,(0,0))
    WIN.blit(LEIA_ORGANA,(1000,363))
    WIN.blit(DARTH_VADER,(400,353))
    draw_ben(ben, ben_direction, ben_jumping)
    
def jump(luke):
    global jumping, Y_VELOCITY
    if jumping:
        luke.y -= Y_VELOCITY
        Y_VELOCITY -= Y_GRAVITY
        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT


def main():
    Y_GRAVITY = 1
    JUMP_HEIGHT = 20
    Y_VELOCITY = JUMP_HEIGHT
    luke = p.Rect(300, 362, LUKE_WIDTH, LUKE_HEIGHT)
    ben = p.Rect(800, 363, LUKE_WIDTH, LUKE_HEIGHT)
    luke_direction = "right"
    ben_direction = "right"
    run = True
    jumping = False
    ben_jumping = False
    clock = p.time.Clock()

    while run:
        clock.tick(FPS)
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False

        keys_pressed = p.key.get_pressed()
        if keys_pressed[p.K_a]: #LEFT
            luke_direction = "left"
        if keys_pressed[p.K_d]: #RIGHT     
            luke_direction = "right"
        if keys_pressed[p.K_LEFT]: #LEFT
            ben_direction = "left"
        if keys_pressed[p.K_RIGHT]: #RIGHT     
            ben_direction = "right"
        if keys_pressed[p.K_SPACE]:
            jumping = True
        if keys_pressed[p.K_UP]:
            ben_jumping = True

        if jumping:
            luke.y -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY
            if Y_VELOCITY < -JUMP_HEIGHT:
                jumping = False
                Y_VELOCITY = JUMP_HEIGHT
        if ben_jumping:
            ben.y -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY
            if Y_VELOCITY < -JUMP_HEIGHT:
                ben_jumping = False
                Y_VELOCITY = JUMP_HEIGHT
       
        LUKE.person_movement(keys_pressed, luke)
        # ben_movement(keys_pressed, ben)
        draw_window(ben_direction,ben,ben_jumping)
        LUKE.draw_person(luke_direction,luke,p.K_k,keys_pressed,jumping,WIN,7,77)
        p.display.update()
    p.quit()
if __name__ == "__main__":
    main()
            