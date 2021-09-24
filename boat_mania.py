import pygame
from pygame.locals import *
import random, time
import tkinter as tk
from tkinter import messagebox
import winsound
from pygame import mixer
from time import sleep

#Initializing
mixer.init()
pygame.init()

collided = False
score = 0
last_tick = pygame.time.get_ticks()

#Setting up FPS to limit the number of executions per second
FPS = 60 # Execute the loop 60 times a second
FramePerSec = pygame.time.Clock()

#Creating colors 
RED   = (255, 0, 0)
WHITE = (255, 255, 255)

#Create a screen with background 
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Boat Mania")
bg = pygame.image.load("images/boat_mania_bg.png")
  

class Enemy(pygame.sprite.Sprite): # Rocket ship
    def __init__(self):
        super().__init__() 
        self.images = [] # Image list 
        self.index = 0
        # Images for creating animation
        self.images.append(pygame.image.load("images/boat1.png"))
        self.images.append(pygame.image.load("images/boat1.png"))
        self.images.append(pygame.image.load("images/boat1.png"))
        self.images.append(pygame.image.load("images/boat1.png"))
        self.images.append(pygame.image.load("images/boat1.png"))
        self.image = self.images[0]
        self.surf = pygame.Surface((50, 65)) 
        self.size = self.image.get_size()
        self.rect = self.surf.get_rect(center = (random.randint(40, 900),0))
         
    def move(self):
        global collided
        global score
        if collided: # Pause the game for 2 second if collided
            time.sleep(2)
        self.rect.move_ip(0,5)
        # Start a new enemy if collided or crosses the window
        if self.rect.bottom > 600 or collided: 
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
            collided = False
            score += 1
            engageSound = mixer.Sound("kachingwav.wav")
            mixer.Sound.play(engageSound)



        # Move the enmey to top if it crosses the window
        if self.rect.bottom > 600 or collided: 
            self.rect.top = 0
            self.rect.center = (random.randint(40, 850), 0)
        
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 1)
        # Change image size
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        surface.blit(self.image, self.rect) 
 
 
class Player(pygame.sprite.Sprite): # Main character
    def __init__(self):
        super().__init__() 
        self.images = []
        self.index = 0
        self.images.append(pygame.image.load('images/avatar1.png'))
        self.images.append(pygame.image.load('images/avatar2.png'))
        self.images.append(pygame.image.load('images/avatar3.png'))
        self.images.append(pygame.image.load('images/avatar4.png'))
        self.image = self.images[0]
        self.surf = pygame.Surface((120, 120)) 
        self.rect = self.surf.get_rect(center = (400, 450)) 
        self.size = self.image.get_size()
    
    def update(self): # Move player on keypress
        pressed_keys = pygame.key.get_pressed()
        # Image selection index from the list
        if self.index:
            self.index = 0
        else:
            self.index = 1
        if self.rect.left > 0: # Move and animate character on keypress
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
                  self.image = self.images[self.index]

        if self.rect.right < 1000: # Move and animate character on keypress       
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  self.image = self.images[self.index]
 
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect, 2) # Check it
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        surface.blit(self.image, self.rect)  





#Setting up Sprites        
P1 = Player()
E1 = Enemy()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

while True:
    # Quit game on pressing the close button
    for event in pygame.event.get():              
        if event.type == pygame.QUIT:
            pygame.quit()
    
    screen.blit(bg, (0, 0))
    if not collided:
        P1.update()
        E1.move()


        
    # Show game over when player collides with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        bg = pygame.image.load("images/boatmaniagmbg.png")
        engageSound = mixer.Sound("lose.wav")
        mixer.Sound.play(engageSound)
        collided = True
        
    P1.draw(screen)
    E1.draw(screen)
    
    # Display score
    font = pygame.font.Font(None, 24)
    scoretext = font.render('Score: '+str(score), True, (0,0,0))
    textRect = scoretext.get_rect()
    textRect.topleft=[20,10]
    screen.blit(scoretext, textRect)
    
    pygame.display.update()
    FramePerSec.tick(FPS) 
