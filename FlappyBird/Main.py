import pygame

#Initialize pygame
pygame.init()

#Import keystrokes
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#Create a screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Create a vector variable to implement gravity
vec = pygame.math.Vector2

#Create a player class
class Player(pygame.sprite.Sprite):
    #Initialize the player
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('FlappyBird/Bird.png')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.acceleration = vec(0, 0.5)  
        self.velocity = vec(0, 0)
        self.position = vec(((SCREEN_WIDTH // 2) - 100, SCREEN_HEIGHT // 2))

    #Move player up when up key is pressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.velocity.y = -5  

        #Apply gravity to the player
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.midbottom = self.position

        #Make sure the player cannot go above the screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y = 2

        #Make sure the player cannot go below the screen
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Create a clock object to control the frame rate
clock = pygame.time.Clock()  

#Create game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    #Get pressed keys while the game is running
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    #Fill the screen with a shade of blue
    screen.fill((0, 200, 255)) 
    
    #Put the player onto the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #Update the display
    pygame.display.flip()

    #Cap the frame rate to 60 frames per second
    clock.tick(60)

pygame.quit()