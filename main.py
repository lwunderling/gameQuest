# This file was created by: Chris Cozort
# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
# Sources: 

'''
Lore for last week:
Functions, methods, Classes, scope('global' vs local)
For loops, break, pass, % modulu, 
string and list traversal

Lore for this week:

GitHub, Modularity, import as

'''



# import libs
import pygame
import random
import os
from settings import *
from pygame.sprite import Sprite
# # global variables
# RUNNING = True
# # screen dims
# WIDTH = 800
# HEIGHT = 600
# # frames per second
# FPS = 30
# # colors
# WHITE = (255, 255, 255)
# BLACK = (0,0,0)
# REDDISH = (240,64,64)
# GREEN = (64,230,64)
# GRAVITY = 9.8

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")



def get_mouse_now():
    x,y = pygame.mouse.get_pos()
    return (x,y)

# classes for game

class Player(Sprite):
    # sprite for player
    # properties of the class
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(BLACK)
        '''sets image path to correct location joining image folder to file name then converting to a more efficient format'''
        # self.image = pygame.image.load(os.path.join(img_folder, "Tie.png")).convert()
        '''sets transparent color key to black'''
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # self.screen_rect = screen.get_rect()
        self.vx = 0
        self.vy = 0
        self.cofric = 0.1
        self.canjump = False
    # stuff it can do....
    def friction(self):
        # print("friction...")
        # if self.vx > -0.5 or self.vx < 0.5:
        #     print("velocity is in range...")
        #     self.vx = 0
        if self.vx > 0.5:
            self.vx -= self.cofric
        elif self.vx < -0.5:
            self.vx += self.cofric
        else:
            self.vx = 0
        if self.vy > 0.5:
            self.vy -= self.cofric
        elif self.vy < -0.5:
            self.vy += self.cofric
        else:
            self.vy = 0
    def gravity(self, value):
        self.vy += value
    def update(self):
        # print(self.vx)
        self.friction()
        if self.rect.bottom < HEIGHT:
            self.gravity(GRAVITY)
        self.rect.x += self.vx
        self.rect.y += self.vy
        # if self.rect.right > WIDTH:
        #     self.rect.x = -50
        #     print("running off screen")
        # if self.rect.top > 500:
        #     self.vy = -5
        # if self.rect.top < 100:
        #     self.vy = 5
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.vy -= 10
        if keystate[pygame.K_a]:
            self.vx -= 10
        if keystate[pygame.K_s]:
            self.vy += 10
        if keystate[pygame.K_d]:
            self.vx += 10
        if keystate[pygame.K_SPACE]:
            self.jump()
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            # print("touched the right side...")
        if self.rect.left < 0:
            self.rect.left = 0
            # print("touched the left side...")
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.canjump = True
            # print("touched the bottom")
        if self.rect.top < 0:
            self.rect.top = 0
            # print("touched the top")
    def jump(self):
        if self.canjump == True:
            self.canjump = False
            self.vy -= 50
            print(self.vy)


class Enemy(Sprite):
    # sprite for player
    # properties of the class
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((50,50))
        self.image.fill(GREEN)
        '''sets image path to correct location joining image folder to file name then converting to a more efficient format'''
        # self.image = pygame.image.load(os.path.join(img_folder, "Tie.png")).convert()
        '''sets transparent color key to black'''
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        # self.screen_rect = screen.get_rect()
        self.vx = 5
        self.vy = 5
        self.cofric = 0.5
    # stuff it can do....
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.right > WIDTH:
            self.vx*=-1
            self.rect.y += 10
            self.rect.x = WIDTH - 50
        if self.rect.left < 0:
            self.vx*=-1
            self.rect.y += 10
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0

    def jump(self):
        print("I jumped...")

# init pygame and create window
pygame.init()
# init sound mixer
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first game...")
clock = pygame.time.Clock() 

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
# testSprite = Sprite()
# testSprite.image = pygame.Surface((50,50))
# testSprite.image.fill(GREEN)
# testSprite.rect = testSprite.image.get_rect()
# testSprite.rect.center = (WIDTH / 2, HEIGHT / 2)
all_sprites.add(player)
# all_sprites.add(testSprite)

for i in range(0,100):
    print(i)
    i = Enemy()
    i.rect[0] = random.randint(0,WIDTH-25)
    i.rect[1] = random.randint(0,HEIGHT)
    enemies.add(i)
    all_sprites.add(i)

# game loop


while RUNNING:
    #  keep loop running at the right speed
    clock.tick(FPS)
    ### process input events section of game loop
    for event in pygame.event.get():
        # check for window closing
        if event.type == pygame.QUIT:
            RUNNING = False
            # break
    # print(get_mouse_now())
    ### update section of game loop (if updates take longer the 1/30th of a second, you will get laaaaag...)
    all_sprites.update()

    blocks_hit_list = pygame.sprite.spritecollide(player, enemies, True)
    for block in blocks_hit_list:
        print(enemies)
    ### draw and render section of game loop
    screen.fill(REDDISH)
    all_sprites.draw(screen)
    # double buffering draws frames for entire screen
    pygame.display.flip()
    # pygame.display.update() -> only updates a portion of the screen
# ends program when loops evaluates to false
pygame.quit()
# Im trying to build a game based off of this where you drop things into moving baskets for points
# # import sys
# import pygame

# pygame.init()

# screen_width = 640
# screen_height = 480
# screen = pygame.display.set_mode((screen_width, screen_height))
# screen_rect = screen.get_rect()

# clock = pygame.time.Clock()

# fps = 60


# class Character(object):
#     def __init__(self, surface, velo, accel, gravity, friction):
#         self.surface = surface
#         self.velo = velo
#         self.accel = accel
#         self.gravity = gravity
#         self.friction = friction
#         self.timestep = 1/fps
#         self.vel = (0, 0)
#         self.pos = ((screen_width / 2), (screen_height / 2))
#         self.size = (20, 20)
        

#     def velocity_right(self):
#         self.pos = (self.pos[0] + self.velo, self.pos[1])

#     def velocity_left(self):
#         self.pos = (self.pos[0] - self.velo, self.pos[1])

#     def velocity_up(self):
        
#         self.pos = (self.pos[0], self.pos[1] - self.velo)

#     def velocity_down(self):
#         self.pos = (self.pos[0], self.pos[1] + self.velo)

#     def velocity(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_i]:
#             self.velocity_up()
#         if keys[pygame.K_j]:
#             self.velocity_left()
#         if keys[pygame.K_k]:
#             self.velocity_down()
#         if keys[pygame.K_l]:
#             self.velocity_right()

#     def accelerate_right(self):
#         self.vel = (self.vel[0] + self.accel, self.vel[1])
#         self.pos = (self.pos[0] + self.vel[0], self.pos[1])

#     def accelerate_left(self):
#         self.vel = (self.vel[0] - self.accel, self.vel[1])
#         self.pos = (self.pos[0] + self.vel[0], self.pos[1])

#     def accelerate_up(self):
#         self.vel = (self.vel[0], self.vel[1] - self.accel)
#         self.pos = (self.pos[0], self.pos[1] + self.vel[1])

#     def accelerate_down(self):
#         self.vel = (self.vel[0], self.vel[1] + self.accel)
#         self.pos = (self.pos[0], self.pos[1] + self.vel[1])
#     def accelerate(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_w]:
#             self.accelerate_up()
#         if keys[pygame.K_a]:
#             self.accelerate_left()
#         if keys[pygame.K_s]:
#             self.accelerate_down()
#         if keys[pygame.K_d]:
#             self.accelerate_right()

#         if self.pos[0] <= 0 or self.pos[0] >= screen_width:
#             self.vel = (self.vel[0] * -1, self.vel[1])

#         if self.pos[1] <= 0 or self.pos[1] >= screen_height:
#             self.vel = (self.vel[0], self.vel[1] * -1)

#         self.character = pygame.Rect((self.pos[0], self.pos[1]), self.size)
#         self.character.clamp_ip(screen_rect)

#     def display(self):
#         pygame.draw.rect(self.surface, (255, 255, 255), self.character)

#     def reset(self):
#         (x_pos, y_pos) = pygame.mouse.get_pos()
#         self.pos = (x_pos, self.pos[1])
#         self.pos = (self.pos[0], y_pos)
#         self.vel = (0, 0)
#     def apply_gravity(self):
#         self.vel = (self.vel[0], self.vel[1] + self.accel)
#         self.pos = (self.pos[0], self.pos[1] + self.vel[1])
#         # self.vel = (self.vel[0], self.vel[1] + self.gravity * self.timestep)
#         # self.pos = (self.pos[0], self.pos[1] + self.vel[1] * self.timestep + 0.5 * self.gravity * self.timestep**2)

#     def apply_friction(self):
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_w] or keys[pygame.K_i]:
#             self.vel = (self.vel[0], self.vel[1] + self.friction)
#             self.pos = (self.pos[0], self.pos[1] + self.vel[1])
#         if keys[pygame.K_a] or keys[pygame.K_j]:
#             self.vel = (self.vel[0] + self.friction, self.vel[1])
#             self.pos = (self.pos[0] + self.vel[0], self.pos[1])
#         if keys[pygame.K_s] or keys[pygame.K_k]:
#             self.vel = (self.vel[0], self.vel[1] - self.friction)
#             self.pos = (self.pos[0], self.pos[1] + self.vel[1])
#         if keys[pygame.K_d] or keys[pygame.K_l]:
#             self.vel = (self.vel[0] - self.friction, self.vel[1])
#             self.pos = (self.pos[0] + self.vel[0], self.pos[1])
# def main():
#     player1 = Character(screen, 10, 1, .5, .4)
#     while True:
#         for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()
#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     player1.reset()

#         player1.apply_gravity()
#         player1.apply_friction()

#         player1.velocity()
#         player1.accelerate()

#         screen.fill((0, 0, 0))

#         player1.display()

#         pygame.display.update(screen_rect)
#         clock.tick(fps)

# if __name__ == "__main__":
#     main()