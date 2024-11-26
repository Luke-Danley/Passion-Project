#import pygame
import pygame

#intialize pygame
pygame.init()

#import keystrokes
from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#create a screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#set background image
background = pygame.image.load('FlappyBird/FlappyBackground.png')

#create game loop
running = True

while running:
    for event in pygame.event.get():
        #close the game if the user hits escape or closes the window
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    #put the background on the screen
    screen.blit(background, (0, 0))

    #update display
    pygame.display.flip()    
