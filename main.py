import os
import pygame
import main2
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("STARWARS")
WIDTH, HEIGHT = 1280,600
FPS = 60
PLAYER_VEL = 5

CRASH_SOUND = pygame.mixer.Sound("audio\crash.mp3")
BLASTER_SOUND = pygame.mixer.Sound("audio/blaster.mp3")
LIGHSTABER_SOUND = pygame.mixer.Sound("audio/lightsaber.mp3")

font = pygame.font.SysFont("arialwhite", 40)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x,y))


window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    """"""
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, width, height, direction = False):
    path = join("postacie", dir1)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(surface) #TUTAJ

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites  

def get_block(size):
    path = join("miejsca","sand1.jpg")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return surface 

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 10

    def __init__(self, x, y, width, height, max_health, name, attack_method):
        super().__init__()
        self.SPRITES = load_sprite_sheets(name, width, height, True)
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = 'left'
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.shot_count = 0
        self.max_health = max_health
        self.actual_health = max_health
        self.attack_method = attack_method
        self.attack_count = 0
        self.block_count = 0
        

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != 'left':
            self.direction = 'left'
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != 'right':
            self.direction = 'right'
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY )
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.udpate_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def udpate_sprite(self):
        sprite_sheet = "standing"
        if self.block_count == 1:
            sprite_sheet = "block"
        if self.shot_count == 1 and self.attack_method == "shot":
            sprite_sheet = "shot"
        if self.attack_count == 1 and self.attack_method == "lightsaber":
            sprite_sheet = "lightsaber"

        if self.x_vel != 0:
            sprite_sheet = self.name
        if self.y_vel != 0:
            if self.jump_count >= 1:
                sprite_sheet = "jump"
            
            
        
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.udpate()

    def udpate(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))

    def create_bullet(self, direction):
        if self.direction == "left":
            return Bullet(self.rect.left, self.rect.centery -20 , direction)
        if self.direction == "right":
            return Bullet(self.rect.right, self.rect.centery -20 , direction)
        


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

class Bullet(pygame.sprite.Sprite):
    # Initialize the bullet object
    def __init__(self, pos_x, pos_y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = 8 # the speed of the bullet
        self.direction = direction

    # Update the bullet's position
    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed # move the bullet to the right
        elif self.direction == "right":
            self.rect.x += self.speed # move the bullet to the right

def get_background(name):
    image = pygame.image.load(os.path.join('miejsca',name))
    background = pygame.transform.scale(image, (WIDTH, HEIGHT))
    return background

def draw(window, background, player, enemy, second_enemy, objects, bullet_group,
         enemy_bullet_group):
    window.blit(background,(0,0)) 

    for obj in objects:
        obj.draw(window)

    hp_bars(player,enemy, 50, 50, bullet_group, enemy_bullet_group, "lightsaber")
    hp_bars(enemy, player, WIDTH - 200, 50, enemy_bullet_group, bullet_group,"shot")
    hp_bars(second_enemy, player, WIDTH - 200, 90, enemy_bullet_group, bullet_group,"shot")
    if player.actual_health < 0:
        player.kill()
    else:
        player.draw(window)
    if enemy.actual_health < 0:
        enemy.kill()
    else:
        enemy.draw(window)
    if second_enemy.actual_health < 0:
        second_enemy.kill()
    else:
        second_enemy.draw(window)
    

    bullet_group.draw(window)
    enemy_bullet_group.draw(window)
    bullet_group.update()
    enemy_bullet_group.update()
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
        
        collided_objects.append(obj)
    return collided_objects

def getting_shot(player, bullet_group):
    for bullet in bullet_group:
        if pygame.sprite.collide_mask(player, bullet) and player.actual_health >= 0:
            player.actual_health -= 10
            bullet_group.remove(bullet)

def getting_stabbed(player, enemy):
    if pygame.sprite.collide_mask(player, enemy) and enemy.attack_count == 1:
        player.actual_health -= 1

def block_shot(player, bullet_group, enemy_bullet_group):
    for bullet in enemy_bullet_group:
        if pygame.sprite.collide_mask(player, bullet) and player.block_count == 1:
            enemy_bullet_group.remove(bullet)
            if bullet.direction == "left":
                bullet_group.add(player.create_bullet("right"))
            if bullet.direction == "right":
                bullet_group.add(player.create_bullet("right"))
            CRASH_SOUND.play()    
                
                

def handle_move(player, enemy, second_enemy, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    if keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)
    

    handle_vertical_collision(player, objects, player.y_vel)
    handle_vertical_collision(enemy, objects, enemy.y_vel)
    handle_vertical_collision(second_enemy, objects, enemy.y_vel)

def hp_bars(player, enemy, x, y, bullet_group, enemy_bullet_group, attack_method = ""):
    if attack_method == "lightsaber":
        block_shot(player, bullet_group, enemy_bullet_group)
        getting_shot(player, enemy_bullet_group)
    if attack_method == "shot":
        getting_shot(player, enemy_bullet_group)
        getting_stabbed(player, enemy)

    ratio = player.actual_health / player.max_health
    pygame.draw.rect(window, "red",(x, y, 150, 20))
    pygame.draw.rect(window, "green",(x, y, 150 * ratio, 20))

def main(window):
    clock = pygame.time.Clock()
    background = get_background("tatooine.jpg")    

    block_size = 32

    player = Player(100, 100, 126, 217,300, "luke", "lightsaber")
    enemy = Player(1100, 100, 133, 168, 100, "jawaa", "shot")
    enemy2 = Player(900, 100, 133, 168, 100, "jawaa", "shot")
    
    blocks = [Block(i * block_size, HEIGHT - block_size, block_size) for i in range(40)]


    bullet_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    number = 0
    number2 = 0
    run = True
    while run:
        clock.tick(FPS)
        number += 1
        number2 += 1
        

        if number % 120 == 0 and enemy.actual_health > 0:
            enemy_bullet_group.add(enemy.create_bullet("left"))
            BLASTER_SOUND.play()
            # player.block_count = 0
        if number % 120 == 60 and enemy2.actual_health > 0:
            enemy_bullet_group.add(enemy2.create_bullet("left"))
            BLASTER_SOUND.play()
            

        if number2 % 5 == 0:
            player.attack_count = 0
        if number2 % 20 == 0:
            player.block_count = 0

        if enemy.actual_health < 0 and enemy2.actual_health < 0: 
            main2.main(window)
        if player.actual_health < 0:
            pygame.quit()
            print("YOU LOST")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k and player.shot_count == 1 and player.attack_method == "shot":
                    bullet_group.add(player.create_bullet())
                if event.key == pygame.K_k and player.attack_method == "shot":
                    number2 = 0
                    player.shot_count = player.shot_count * (-1) + 1
                if event.key == pygame.K_k and player.attack_method == "lightsaber":
                    number2 = 0
                    LIGHSTABER_SOUND.play()
                    player.attack_count = player.attack_count * (-1) + 1
                if event.key == pygame.K_b:
                    player.block_count = player.block_count * (-1) + 1
            

        
        player.loop(FPS)
        enemy.loop(FPS)
        enemy2.loop(FPS)
        handle_move(player,enemy,enemy2, blocks)
        draw(window, background, player, enemy, enemy2, blocks, bullet_group,enemy_bullet_group)
        draw_text("press space to play", font, (255,255,255), 160, 250)
    pygame.quit()
    quit()
    

if __name__ == "__main__":
    main(window)
