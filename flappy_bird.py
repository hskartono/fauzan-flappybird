import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up screen
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

bird_images = [
    pygame.image.load("flappybird_up.png"),
    pygame.image.load("flappybird_mid.png"),
    pygame.image.load("flappybird_down.png")
]
animation_index = 0
background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Define game variables
bird_x = 50
bird_y = screen_height // 2
bird_velocity = 0
gravity = 0.25
jump_velocity = -7
bird_radius = 20

# Set up pipe
pipe_top_img = pygame.image.load("pipe_top.png")
pipe_bottom_img = pygame.image.load("pipe_bottom.png")
pipe_width = pipe_top_img.get_width()
pipe_gap = 150
pipe_velocity = 3
pipes = []

# Set up font
font = pygame.font.SysFont("Arial", 30)

# Function to draw the bird
def draw_bird():
    global animation_index
    bird_image = bird_images[animation_index]
    screen.blit(bird_image, (bird_x, bird_y))
    animation_index = (animation_index + 1) % len(bird_images)

# Function to draw pipes
def draw_pipes():
    for pipe in pipes:
        screen.blit(pipe_top_img, (pipe['top'].x, pipe['top'].y))
        screen.blit(pipe_bottom_img, (pipe['bottom'].x, pipe['bottom'].y))

# Function to move pipes
def move_pipes():
    for pipe in pipes:
        pipe['top'].x -= pipe_velocity
        pipe['bottom'].x -= pipe_velocity

# Function to check for collisions
def check_collisions():
    global bird_y
    if bird_y <= 0 or bird_y >= screen_height:
        return True
    for pipe in pipes:
        if pipe['top'].colliderect(pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)) or pipe['bottom'].colliderect(pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)):
            return True
    return False

# Function to generate pipes
def generate_pipes():
    # Set minimum and maximum height for the top pipe to avoid it being too short
    min_pipe_height = 200
    max_pipe_height = 400
    
    # Random height within defined limits for the top pipe
    pipe_height = random.randint(min_pipe_height, max_pipe_height)
    
    # Calculate position of the top and bottom pipes based on the gap
    # top_rect = pipe_top_img.get_rect(topleft=(screen_width, pipe_height - pipe_top_img.get_height()))
    top_rect = pipe_top_img.get_rect(topleft=(screen_width, 0))
    bottom_rect = pipe_bottom_img.get_rect(topleft=(screen_width, pipe_height + pipe_gap))
    
    # Append pipes with consistent gap and controlled height
    pipes.append({'top': top_rect, 'bottom': bottom_rect})

# Main game loop
live = 3
while live > 0:
    running = True
    bird_x = 50
    bird_y = screen_height // 2
    bird_velocity = 0
    gravity = 0.25
    jump_velocity = -7
    bird_radius = 20
    pipes = []
    string_number = str(live)
    pygame.display.set_caption("Flappy Bird, Live:" + string_number)
    print("live", string_number)
    print("running", running)
    while running:
        # Draw the background
        screen.blit(background_img, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_velocity

        # Update bird position
        bird_velocity += gravity
        bird_y += bird_velocity
        
        # Update pipes and check collisions
        move_pipes()
        if check_collisions():
            running = False

        # Generate new pipes
        if len(pipes) == 0 or pipes[-1]['top'].x < screen_width - 200:
            generate_pipes()

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['top'].x + pipe_width > 0]

        # Draw everything
        draw_bird()
        draw_pipes()

        # Update the screen
        pygame.display.update()
        pygame.time.Clock().tick(60)
    live = live - 1

pygame.quit()
sys.exit()
