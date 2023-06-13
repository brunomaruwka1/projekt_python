import pygame
import button
import main

pygame.init()


WIDTH, HEIGHT = 1280,600
FPS = 60
TEXT_COLOR = (219, 172, 52)


COSMOS_IMAGE = pygame.image.load("miejsca\cosmos.png")
STARWARS_SIGN = pygame.image.load("miejsca\starwars_sign.png")
STARWARS_SIGN = pygame.transform.scale(STARWARS_SIGN, (400, 250))


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu")

font = pygame.font.SysFont("Italic", 40)

game_paused = True

STAR_WARS_THEME_SONG = pygame.mixer.Sound("audio\STARWARS_themesong.mp3")
STAR_WARS_THEME_SONG.play()  # -1 oznacza zapętlenie odtwarzania

#load buttons images
resume_img = pygame.image.load("guziki/button_resume.png").convert_alpha()
quit_img = pygame.image.load("guziki/button_quit.png").convert_alpha()
back_img = pygame.image.load('guziki/button_back.png').convert_alpha()
#create buttons instances
resume_button = button.Button(545, 280, resume_img, 1)
back_button = button.Button(572, 370, back_img, 1)
quit_button = button.Button(576, 460, quit_img, 1)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

run = True
while run:


    window.blit(COSMOS_IMAGE, (0,0))
    window.blit(STARWARS_SIGN, (440,50))
    

    if game_paused == True:
        if resume_button.draw(window):
            game_paused = False
        quit_button.draw(window)
        back_button.draw(window)
        
    else:
        main.main(window)
        game_paused = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()