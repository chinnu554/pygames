import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Ray Edition")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game clock
clock = pygame.time.Clock()
FPS = 60

# Bird settings
bird_x = 60
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.5
flap_strength = -8

# Pipe settings
pipe_width = 60
pipe_gap = 150
pipe_speed = 3
pipes = []

# Score
score = 0
font = pygame.font.SysFont("Arial", 32)
game_over = False

def create_pipe():
    top_height = random.randint(50, 300)
    bottom_y = top_height + pipe_gap
    return {"top": pygame.Rect(WIDTH, 0, pipe_width, top_height),
            "bottom": pygame.Rect(WIDTH, bottom_y, pipe_width, HEIGHT - bottom_y)}

def show_text(text, size, color, y_offset=0):
    font_obj = pygame.font.SysFont("Arial", size, bold=True)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def show_home_page():
    screen.fill(BLUE)
    show_text("Flappy Bird", 48, YELLOW, -40)
    show_text("Press SPACE to Start", 28, WHITE, 40)
    pygame.display.flip()
    wait_for_space()

def wait_for_space():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def reset_game():
    global bird_y, bird_velocity, pipes, score, game_over
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    score = 0
    game_over = False

# Show home page
show_home_page()

# Main Game Loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                bird_velocity = flap_strength
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()

    if not game_over:
        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)

        # Pipe movement and collision
        for pipe in pipes:
            pipe["top"].x -= pipe_speed
            pipe["bottom"].x -= pipe_speed

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe["top"].x + pipe_width > 0]

        # Add new pipes
        if not pipes or pipes[-1]["top"].x < WIDTH - 200:
            pipes.append(create_pipe())

        # Check for collisions and scoring
        for pipe in pipes:
            if bird_rect.colliderect(pipe["top"]) or bird_rect.colliderect(pipe["bottom"]):
                game_over = True
            if pipe["top"].x + pipe_width < bird_x and not pipe.get("scored", False):
                score += 1
                pipe["scored"] = True

        # Check if bird hits ground or goes off screen
        if bird_y - bird_radius < 0 or bird_y + bird_radius > HEIGHT:
            game_over = True

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe["top"])
            pygame.draw.rect(screen, GREEN, pipe["bottom"])

        # Draw bird
        pygame.draw.circle(screen, RED, (bird_x, int(bird_y)), bird_radius)

        # Draw ground line
        pygame.draw.rect(screen, (139, 69, 19), (0, HEIGHT - 20, WIDTH, 20))

        # Score display
        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))

    else:
        show_text("Game Over", 48, RED, -30)
        show_text(f"Score: {score}", 32, WHITE, 20)
        show_text("Press SPACE to Retry", 24, WHITE, 60)

    pygame.display.flip()

pygame.quit()
