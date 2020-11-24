# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:54:32 2020

@author: hungd
"""

import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

# Load images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
          
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    def __init__(self, x, y):
        self.x = x     # x position (top-left is (0,0))
        self.y = y     # y position (top-left is (0,0))
        self.tilt = 0  # tilt of the bird
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        
    def jump(self):
        self.vel = -10.5 
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        
        ###########################################################################################################
        # d = vt + 1/2 at^2 (In this case, acceleration = 3)                                                      #
        # Remember up is the negative y direction so initial vel is negative; therefore, acceleration is positive #
        # It's the opposite of on earth                                                                           #
        # Displacement is in pixels                                                                               #
        ###########################################################################################################
        
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        
        # Set Maximum "acceleration" really we are doing maximum displacement
        if d >= 16:
            d = 16
        
        # Make the bird look like it has a little more hang time than it should
        if d < 0:
            d -= 2
            
        # Change the y position
        self.y = self.y + d
        
        # Make the bird tilt up
        # The bird should have max tilt at least 50 pixels above initial jump or anytime the bird is still going up
        if d < 0  or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:  # -90 is a nose dive
                self.tilt -= self.ROT_VEL
                
    def draw(self, win):
        self.img_count += 1
        
        # This makes the bird look like it is flapping it's wings.  The wings open then close then resets
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        # Don't want the bird to flap it's wings anymore once the tilt is less than -80
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2
            
        # Rotate image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)  # blit is draw
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    

def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))  # Draw the background starting at the top-left
    bird.draw(win)
    pygame.display.update()
    
      
def main():
    bird = Bird(200, 200)  # initial position of the bird
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
         
        # bird.move()
        draw_window(win, bird)
     
    pygame.quit()
    quit()
    
main()
        
            
            
                
        
        
        
        
        
        
        