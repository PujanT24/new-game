import pygame
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Among us sample")
clock = pygame.time.Clock()
"""
start_screen = pygame.image.load("assets/start_screen.png").convert_alpha
play_btn = pygame.image.load("assets/start.png").convert_alpha
play_rect = play_btn.get_rect(center = (400, 350))
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/amongus.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200,400))
        self.gravity = 0
        self.speed = 6

    def jump (self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 400:
            self.gravity = -20

    def fall(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400

    def right(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.speed


    def left(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
    



    def update(self):
        self.jump()
        self.fall()
        self.right()
        self.left()

class Target(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = random.randint(800,1000)
        if type == "imposter":
            self.image = pygame.image.load("assets/imposter.png").convert_alpha()
        else:
            self.image = pygame.image.load("assets/safe.png").convert_alpha()
        self.rect = self.image.get_rect(center = (self.start, 330))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def check_collisions():
    global score
    if player.sprite:
        collided_targets = pygame.sprite.spritecollide(player.sprite, target_group, True)
        if collided_targets:
            score += 1

game_screen = 1
score = 0
score_font = pygame.font.Font(None,30)

def display_score():
    score_surf = score_font.render("Score:" + str(score), True, (50,50,50))
    score_rect = score_surf.get_rect(center = (100, 50))
    screen.blit(score_surf, score_rect)




target_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
player.add(Player())

ground = pygame.image.load("assets/grass.png").convert()
soil = pygame.image.load("assets/soil.png").convert()
sky = pygame.image.load("assets/sky.png").convert()
while True:
    for event in pygame.event. get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen .blit(ground, (0,350))
    screen .blit(soil, (0,400))
    screen .blit(sky, (0,0))  

    target_group.draw(screen)

    target_group.update()
    if not target_group:
        i = random.randint(0,1)
        choices = ['imposter','safe']
        target_group.add(Target(choices[i]))     

    player.update()
    player.draw(screen)
    check_collisions()
    display_score()
    pygame.display.update()
    clock.tick(60)
