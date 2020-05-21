# This file was created by: Chris Cozort
# Sources: http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/
# Sources: https://techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-collision/
# Sources: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
# Sources: https://www.pixilart.com/draw
# sources: https://www.geeksforgeeks.org/python-display-images-with-pygame/
# Sources: https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
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
import time
# from settings import *
from pygame.sprite import Sprite

TITLE = "Jump and score"
WIDTH = 480
HEIGHT = 600
FPS = 60
RUNNING = True
# Environment options
GRAVITY = 9.8

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.01
PLAYER_JUMPPOWER = 10

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 247)
ORANGE = (255, 187, 0)
YELLOW = (255, 255, 0)
score = 0
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
        # self.image = pygame.image.load(r"basketball.png")
        # self.image.fill(BLACK)
        '''sets image path to correct location joining image folder to file name then converting to a more efficient format'''
        self.image = pygame.image.load(os.path.join(img_folder, "basketball2.png")).convert()
        #scaling the sprite image
        self.image = pygame.transform.scale(self.image, (40, 40))
        '''sets transparent color key to black'''
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (25, HEIGHT - 25)
        # self.screen_rect = screen.get_rect()
        self.vx = 0
        self.vy = 0
        self.cofric = .2
        self.canjump = False
        #Making player movement stop when hits platform
        self.blocked = False
    # stuff it can do....
    def friction(self):
        # print("friction...")
        # if self.vx > -0.5 or self.vx < 0.5:
        #     print("velocity is in range...")
        #     self.vx = 0
        #Velocity cannot be higher than .5 or slower than -.5
        if self.vx > .5:
            self.vx -= self.cofric
        elif self.vx < -.5:
            self.vx += self.cofric
        else:
            self.vx = 0
        if self.vy > 1:
            self.vy -= self.cofric
        elif self.vy < -1:
            self.vy += self.cofric
        else:
            self.vy = 0
    def gravity(self, value):
        if self.blocked == False:
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
        #W key slows the sprite's vertical speed down by 10
        if keystate[pygame.K_w]:
            self.vy -= 10
        #A key decreses horozintal speed by 10
        if keystate[pygame.K_a]:
            self.vx -= 6
            #makes it so when you leave the platform gravity starts working again
            player.blocked = False
        #The S Key imcreases the vertical velocity by 10
        if keystate[pygame.K_s]:
            self.vy += 10
        #The D key speeds up the horozintal velocity by 10
        if keystate[pygame.K_d]:
            self.vx += 6
            #makes it so when you leave the platform gravity starts working again
            player.blocked = False
        #Space causes the sprite to jump
        if keystate[pygame.K_SPACE]:
            self.jump()
            player.blocked = False
        #Allows you to toggle settings during the game such as friction and gravity with 1,2,3,4 keys
        # if keystate[pygame.K_1]:
        #     self.cofric += .02
        # if keystate[pygame.K_2]:
        #     self.cofric -= .02
        # if keystate[pygame.K_3]:
        #     GRAVITY += .5
        # if keystate[pygame.K_4]:
        #     GRAVITY -= .5 
        
        #These next four if statements set boundries for the rectange the box is in
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.canjump = True
            
        if self.rect.top < 0:
            self.rect.top = 0
            
    def jump(self):
        #this says if you are currently jumping, then you cant jump again until you are at the bottom of the screen
        if self.canjump == True:
            self.canjump = False
    
            #Decreases the y velocity to pull the cube back down
            self.vy -= 50
            print(self.vy)
#Creating the platform class
class Platform(Sprite):
   def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.Surface((100,20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT-200) 
       #Makes the object hitbox the size of the shape so when sprites collide the edges detect the collision not the center
        self.hitbox = (self.rect.x  , self.rect.y)

class Hoop(Sprite):
   def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "hoop2.png")).convert()
        # self.image = pygame.Surface((200,15))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH-15,150) 
        self.hitbox = (self.rect.x  , self.rect.y)

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
    # stuff it can do.
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
# pygame.display.set_caption("My first game...")
clock = pygame.time.Clock() 

pygame.display.set_caption('Basket Shooter')   
# Choice in font and font size
font = pygame.font.Font('freesansbold.ttf', 32)   
# Choice in what text I want initally displayed 
text = font.render('0', True, ORANGE, PURPLE) 
#Creates the shape of the text box
textRect = text.get_rect()  
# set the center of the rectangular object. 
textRect.center = (50,50) 

# "when player scores change score +1"
# text = font.render('0', True, green, blue) 
screen.blit(text, textRect) 
pygame.display.update()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
hoop = Hoop()
platform = Platform()
all_sprites.add(player)
all_sprites.add(platform)
all_sprites.add(hoop)
# all_sprites.add(testSprite)

for i in range(0,1):
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
    #Creating collosion for the cube and the new platform
    if pygame.sprite.collide_rect(platform, player) and player.blocked == False:
        if player.vy < 0:
            player.vy = -player.vy
        else:
            player.vx = 0
            player.vy = 0
            player.blocked = True
            #allows you to jump when not on the bottom
            player.canjump = True
            #if you set them equal they are alwys in collison making jump not work, making them 1 pixel apart they are no longer in collision
            player.rect.bottom = platform.rect.top -1
    
    if pygame.sprite.collide_rect(hoop, player) and player.blocked == False:
        if player.vy < 0:
            player.vy = -player.vy
        else:
            score = score +1
            screen.fill(RED)
            pygame.display.update() 
            time.sleep(.3)
            screen.fill(WHITE)
            pygame.display.update() 
            # player.vx = 0
            # player.vy = 0
            # #allows you to jump when not on the bottom
            # player.canjump = True
            #if you set them equal they are alwys in collison making jump not work, making them 1 pixel apart they are no longer in collision
            player.rect.bottom = platform.rect.top -1

    ### draw and render section of game loop
    screen.fill(WHITE)
    text = font.render(str(score), True, ORANGE, PURPLE) 
    screen.blit(text, textRect) 
    all_sprites.draw(screen)
    # double buffering draws frames for entire screen
    pygame.display.flip()
    pygame.display.update() 
    # -> only updates a portion of the screen
# ends program when loops evaluates to false
pygame.quit()
