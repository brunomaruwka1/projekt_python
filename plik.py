import pygame  
import os

WIDTH, HEIGHT = 1280,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption("STAR WARS: A NEW HOPE (fan version)")

WHITE = (255,255,255)

FPS = 60

LUKE_WIDTH, LUKE_HEIGHT = 90, 228

VEL = 5

Y_GRAVITY = 1

JUMP_HEIGHT = 20

Y_VELOCITY = JUMP_HEIGHT

jumping = False

LUKE_SKYWALKER_IMAGE = pygame.image.load(os.path.join('postacie','luke_skywalker.png'))
JUMPING_LUKE_SKYWALKER_IMAGE = pygame.image.load(os.path.join('postacie','luke_jumping.png'))

TATOOINE_IMAGE = pygame.image.load(os.path.join('miejsca','tatoine.jpg'))

def draw_window(luke,direction,jumping):
    WIN.blit(TATOOINE_IMAGE,(0,0))
    if jumping == True: 
        if direction == "right":
            WIN.blit(JUMPING_LUKE_SKYWALKER_IMAGE,(luke.x,luke.y))
        if direction == "left":
            character_left_flipped = pygame.transform.flip(JUMPING_LUKE_SKYWALKER_IMAGE, True, False)
            WIN.blit(character_left_flipped, (luke.x, luke.y))

    else:
        if direction == "right":
            WIN.blit(LUKE_SKYWALKER_IMAGE,(luke.x,luke.y))
        if direction == "left":
            character_left_flipped = pygame.transform.flip(LUKE_SKYWALKER_IMAGE, True, False)
            WIN.blit(character_left_flipped, (luke.x, luke.y))
    pygame.display.update()

def luke_movement(keys_pressed, luke):
    if keys_pressed[pygame.K_a]: #LEFT
            luke.x -= VEL
    if keys_pressed[pygame.K_d]: #LEFT
            luke.x += VEL

def main():
    Y_GRAVITY = 1
    JUMP_HEIGHT = 20
    Y_VELOCITY = JUMP_HEIGHT
    luke = pygame.Rect(300, 362, LUKE_WIDTH, LUKE_HEIGHT)
    luke_direction = "right"
    run = True
    jumping = False
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]: #LEFT
            luke_direction = "left"
        if keys_pressed[pygame.K_d]: #RIGHT     
            luke_direction = "right"
        if keys_pressed[pygame.K_SPACE]:
            jumping = True

        if jumping:
            luke.y -= Y_VELOCITY
            Y_VELOCITY -= Y_GRAVITY
            if Y_VELOCITY < -JUMP_HEIGHT:
                jumping = False
                Y_VELOCITY = JUMP_HEIGHT

        luke_movement(keys_pressed, luke)
        draw_window(luke,luke_direction,jumping)
    pygame.quit()
if __name__ == "__main__":
    main()
            