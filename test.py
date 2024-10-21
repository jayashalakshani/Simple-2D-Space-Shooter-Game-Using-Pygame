# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 03:42:27 2023

@author: MyPc
"""

import pygame 
import os

#font types
pygame.font.init()

#sound effects
pygame.mixer.init()

WIDTH,HEIGHT =900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

#chage the toolbar name
pygame.display.set_caption("First Game!")

#COLORS
WHITE=(255,255,255)
BLACK=(0,0,0)
YELLOW=(255,0,0)
RED=(255,255,0)

#creat the border
BORDER = pygame.Rect(WIDTH//2 - 5,0, 10, HEIGHT )

#creat the variable for sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

#font type
HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

#how many frame per second game to update at now
FPS = 60
VEL = 5

#speed of the bullets
BULLET_VEL = 7

#number of bullets
MAX_BULLETS = 3

#spaceship width and height
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 55, 44

#creat the event
YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT +2

#load the images(yellow)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))

#resize & Rotate spaceship(yellow)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)

#load the images(red)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))

#resize & Rotate spaceship(red)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

#Backgorund
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH,HEIGHT))

def draw_window(red, yellow, yellow_bullets,red_bullets,red_health,yellow_health):
    #fill window with specific background image
    WIN.blit(SPACE, (0,0))
    
    #draw the border at middle of the window
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    #show the health text
    red_health_text =HEALTH_FONT.render("Health: "+ str(red_health), 1, WHITE)
    yellow_health_text =HEALTH_FONT.render("Health: "+ str(yellow_health), 1, WHITE)
    
    #draw the health on the screen
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(red_health_text,(WIDTH -red_health_text.get_width() -10,10))
    
    #draw a spaceship on the screen
    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y ))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))
    
    #Draw the bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()

def yellow_handli_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        #left side by pressing key 'a'
        yellow.x -=VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        #right side by pressing key 'd'
        yellow.x +=VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        #up side by pressing key 'w'
        yellow.y -=VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -10:
        #down side by pressing key 's'
        yellow.y +=VEL

def red_handli_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        #left side by pressing key 'LEFT'
        red.x -=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        #right side by pressing key 'RIGHT'
        red.x +=VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        #up side by pressing key 'UP'
        red.y -=VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -10:
        #down side by pressing key 'DOWN'
        red.y +=VEL
        
#handling bullets function.
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        #check whether yellow bullet is collied to red one
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            #if collied need to remove the bullet
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        #check whether red bullet is collied to yellow one
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            #if collied need to remove the bullet
            red_bullets.remove(bullet)
        elif bullet.x <0:
            red_bullets.remove(bullet)
            
#show the winner
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2 -draw_text.get_width()/2, HEIGHT/2 -draw_text.get_height()/2))
    #display the winner
    pygame.display.update()
    #after someone win the game the interface will be close afther 500 milliseconds
    pygame.time.delay(1500)
    
def main():
    #CONTROL THE MOVING OF THE SPACESHIPS
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    
    #CREATE BUTTET LIST 
    yellow_bullets =[]
    red_bullets =[]
    
    red_health =10
    yellow_health =10
    
    clock = pygame.time.Clock()
    
    run = True
    while run:
        #Control the speed of the whilw loop
        clock.tick(FPS)
        
        for event in pygame.event.get():
            #if user want to quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            #control the bullets using keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet =pygame.Rect(yellow.x +yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL  and len(red_bullets) < MAX_BULLETS:
                    bullet =pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            #If bullet hit spaceship what th do
            if event.type == RED_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()
                
        winner_text=""
        if red_health <= 0:
            winner_text ="Yellow Win!"
        if yellow_health <=0:
            winner_text ="Red Win!"
        if winner_text !="":
            draw_winner(winner_text)
            break
        #can use more than one key
        #what is the key pressed at a time
        keys_pressed = pygame.key.get_pressed()
        yellow_handli_movement(keys_pressed, yellow)
        red_handli_movement(keys_pressed, red)
        
        #handle the bullets
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health)
       
    main()
    
if __name__ =="__main__":
    main()