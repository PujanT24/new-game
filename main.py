"""
This is a that helps player to get away from distraction.
To play the player clicks start and then press a and d to move left and right and space to jump and get book and avoid messages to increase focus. 
Written by Pujan Tailor
"""

import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Among us sample")
clock = pygame.time.Clock()


game_screen = 0
focus = 0

# This is a player class.

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk1 = pygame.image.load("assets/walk1.png").convert_alpha()
        walk2 = pygame.image.load("assets/walk2.png").convert_alpha()
        self.player_index = 0
        self.player_walk = [walk1, walk2]
        self.player_jump = pygame.image.load("assets/jump.png").convert_alpha()
        

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,400))
        self.gravity = 0
        self.speed = 6
#This is code to jump
    def jump (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.gravity = -20

    def fall(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 374:
            self.rect.bottom = 374

#This is code to go right
    def right(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.speed

#This is code to go left
    def left(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.rect.x -= self.speed

#This is code to make my character walking animations
    def animations(self):
        if self.rect.bottom < 360:
            self.image = self.player_jump
        else:
            self.player_index += 0.05
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    
    
    def update(self):
        self.animations()
        self.jump()
        self.fall()
        self.right()
        self.left()


player = pygame.sprite.GroupSingle()
player.add(Player())

#This is Target class
class Target(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.start = random.randint(800,1000)
        if type == "kilogram":
            self.image = pygame.image.load("assets/kilogram.png").convert_alpha()
        else:
            self.image = pygame.image.load("assets/book.png").convert_alpha()
        self.rect = self.image.get_rect(center = (self.start, 330))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
#This code check if player collided with something
def check_collisions():
    global focus
    if player.sprite:
        collided_targets = pygame.sprite.spritecollide(player.sprite, target_group, True)
        for target in collided_targets:
            if target.type == "book":
                focus += 1
            else:
                focus -= 1

target_group = pygame.sprite.Group()

focus_font = pygame.font.Font(None,30)

#This code shows focus on the game screen. 
def display_focus():
    focus_surf = focus_font.render("Focus:" + str(focus), True, (50,50,50))
    focus_rect = focus_surf.get_rect(center = (100, 50))
    screen.blit(focus_surf, focus_rect)

#This code 
start_screen = pygame.image.load("assets/start_screen.png").convert_alpha()
play_btn = pygame.image.load("assets/start.png").convert_alpha()
play_rect = play_btn.get_rect(center = (400, 350))

ground = pygame.image.load("assets/grass.png").convert()
soil = pygame.image.load("assets/soil.png").convert()
sky = pygame.image.load("assets/sky.png").convert()

lose = pygame.image.load("assets/end_screen.png").convert()
win = pygame.image.load("assets/win_screen.png").convert()
restart_btn = pygame.image.load("assets/restart.png").convert_alpha()
restart_rect = restart_btn.get_rect(center = (300,350))
quit_btn = pygame.image.load("assets/quit.png").convert_alpha()
quit_rect = quit_btn.get_rect(center = (500,350))


while True:
    for event in pygame.event. get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                game_screen = 1

            if game_screen in (2, 3):
                if play_rect.collidepoint(event.pos):
                    game_screen = 1

            if restart_rect.collidepoint(event.pos):
                focus = 0
                
                game_screen = 1

            if quit_rect.collidepoint(event.pos):
                pygame.quit()
                exit()


    if game_screen == 0:
        screen.blit(start_screen, (0,0))
        screen.blit(play_btn, play_rect)

    elif game_screen == 1:
        screen.blit(ground, (0,350))
        screen.blit(soil, (0,400))
        screen.blit(sky, (0,0))

       
        if not target_group:
            i = random.randint(0,1)
            choices = ['kilogram','book']
            target_group.add(Target(choices[i]))  



        player.update()
        player.draw(screen)
        target_group.draw(screen)
        target_group.update()
        display_focus()
        check_collisions()


        if focus < -5:
            game_screen = 3
        if focus == 10:
            game_screen = 4

    elif game_screen == 4:
        screen.blit(win,(0, 0))
        screen.blit(restart_btn, restart_rect)
        screen.blit(quit_btn, quit_rect)
    

    else:
        screen.blit(lose,(0, 0))
        screen.blit(restart_btn, restart_rect)
        screen.blit(quit_btn, quit_rect)

    pygame.display.update()
    
    pygame.display.update() 
    clock.tick(60)
    
