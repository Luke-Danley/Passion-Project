import pygame

from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    KEYDOWN,
    QUIT,
)

pygame.init()

Screen_Width = 1200
Screen_Height = 800


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("bob.jpg").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        
screen = pygame.display.set_mode((Screen_Width, Screen_Height))


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    screen.fill((135, 206, 250))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()