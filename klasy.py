import pygame as p

class character:
    def __init__(self, width , height, image, attacking_image, jumping_image, vel):
        self.WIDTH = width
        self.HEIGHT = height
        self.IMAGE = image
        self.ATTACKING_IMAGE = attacking_image
        self.JUMPING_IMAGE = jumping_image
        self.VEL = vel
    def draw_person(self,direction,person,key,keys_pressed,jumping,WIN,y=0,x=0):
        if jumping == True: 
            if direction == "right":
                WIN.blit(self.JUMPING_IMAGE,(person.x,person.y))
            if direction == "left":
                character_left_flipped = p.transform.flip(self.JUMPING_IMAGE, True, False)
                WIN.blit(character_left_flipped, (person.x, person.y))
        elif keys_pressed[key]:
                if direction == "left":
                    character_left_flipped = p.transform.flip(self.ATTACKING_IMAGE, True, False)
                    WIN.blit(character_left_flipped, (person.x-x, person.y+y))
                if direction == "right":
                    WIN.blit(self.ATTACKING_IMAGE, (person.x, person.y+7))
        else:
            if direction == "right":
                WIN.blit(self.IMAGE,(person.x,person.y))
            if direction == "left":
                character_left_flipped = p.transform.flip(self.IMAGE, True, False)
                WIN.blit(character_left_flipped, (person.x,person.y))
    def person_movement(self,keys_pressed, luke):
        if keys_pressed[p.K_a]: #LEFT
            luke.x -= self.VEL
        if keys_pressed[p.K_d]: #LEFT
            luke.x += self.VEL


