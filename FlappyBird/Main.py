import pygame
import random

# Initialize pygame
pygame.init()

# Import keystrokes
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Create a screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a vector variable to implement gravity
vec = pygame.math.Vector2

# Create a player class
class Player(pygame.sprite.Sprite):
    # Initialize the player
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load('FlappyBird/Bird.png')
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.acceleration = vec(0, 0.5)
        self.velocity = vec(0, 0)
        self.position = vec(((SCREEN_WIDTH // 2) - 100, SCREEN_HEIGHT // 2))

    # Move player up when up key is pressed
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.velocity.y = -5

        # Apply gravity to the player
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration
        self.rect.midbottom = self.position

        # Make sure the player cannot go above the screen
        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y = 2

        # Make sure the player cannot go below the screen
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0

# Create a pipe at the top of the screen
class PipeTop(pygame.sprite.Sprite):
    speed = 5

    def __init__(self, x_position, gap_y):
        super(PipeTop, self).__init__()
        self.surf = pygame.image.load('FlappyBird/FlippedFlappyBirdPipe.png')
        self.rect = self.surf.get_rect()
        self.rect.bottomleft = (x_position, gap_y)
        self.passed = False

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Create a pipe at the bottom of the screen
class PipeBottom(pygame.sprite.Sprite):
    speed = 5

    def __init__(self, x_position, gap_y, gap_size):
        super(PipeBottom, self).__init__()
        self.surf = pygame.image.load('FlappyBird/FlappyBirdPipe.png')
        self.rect = self.surf.get_rect()
        self.rect.topleft = (x_position, gap_y + gap_size)
        self.passed = False

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize player and pipes
player = Player()

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pipes = pygame.sprite.Group()

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

y = 300
x = 2000
# Timer for adding new pipes
ADD_PIPE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_PIPE_EVENT, x)

# Initialize score
score = 0
# Create game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("Game Over!")
                print("You Scored: " + str(score // 2))
                running = False
        elif event.type == QUIT:
            print("Game Over!")
            print("You Scored: " + str(score // 2))
            running = False
        elif event.type == ADD_PIPE_EVENT:
            if (score // 2) % 5 == 0 and score != 0:
                x -= 200
                if x <= 600:
                    x = 600
                pygame.time.set_timer(ADD_PIPE_EVENT, x)
            if (score // 2) % 10 == 0:
                y -= 50
                if y <= 175:
                    y = 175
            gap_size = random.randint(175, y)
            gap_y = random.randint(100, SCREEN_HEIGHT - 100 - gap_size)
            new_pipe_top = PipeTop(SCREEN_WIDTH, gap_y)
            new_pipe_bottom = PipeBottom(SCREEN_WIDTH, gap_y, gap_size)
            all_sprites.add(new_pipe_top)
            all_sprites.add(new_pipe_bottom)
            pipes.add(new_pipe_top)
            pipes.add(new_pipe_bottom)

    # Get pressed keys while the game is running
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update pipes
    pipes.update()

    # Check for collisions
    if pygame.sprite.spritecollideany(player, pipes):
        print("Game Over!")
        print("You Scored: " + str(score // 2))
        running = False

    # Check if the player passes a pipe
    for pipe in pipes:
        if pipe.rect.right < player.rect.left and not pipe.passed:
            pipe.passed = True
            score += 1

    # Fill the screen with a shade of blue
    screen.fill((0, 200, 255))

    # Put the player onto the screen
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Display Score
    font = pygame.font.Font(None, 74)
    text = font.render(str(score // 2), 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 frames per second
    clock.tick(60)

pygame.quit()