
import pygame
import random

pygame.init()
pygame.font.init()

# Pencere ayarları
screen = pygame.display.set_mode((600, 600))
game_surface = pygame.Surface((600, 600))
vhs_surface = pygame.Surface((600, 600))
pygame.display.set_caption("Neon Snake")
clock = pygame.time.Clock()

# Yazı tipi
font = pygame.font.SysFont("Arial", 43, bold=True)
title_font = pygame.font.SysFont("Courier New", 25, bold=True)
small_font = pygame.font.SysFont("Courier New", 24)


# Oyun alanı
CELL_SIZE = 20
GRID_WIDTH = 600 // CELL_SIZE
GRID_HEIGHT = 600 // CELL_SIZE

# Yılan
snake = [
    (300, 300),
    (280, 300),
    (260, 300)
]

direction = (20, 0)

# Yem oluşturma
def create_food():
    while True:
        food = (
            random.randint(5, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(5, GRID_HEIGHT - 1) * CELL_SIZE
        )
        if food not in snake:
            return food

food = create_food()

# Hareket ayarları
move_delay = 100
last_move_time = 0

running = True
game_over = False
game_started = False
score = 0
blink_timer = 0
show_prompt = True
glow_surface = pygame.Surface((600, 600), pygame.SRCALPHA)
flicker = False
# Ana oyun döngüsü
while running:

    # Olayları kontrol et
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = True

            if event.key == pygame.K_w and direction != (0, 20):
                direction = (0, -20)

            if event.key == pygame.K_s and direction != (0, -20):
                direction = (0, 20)

            if event.key == pygame.K_a and direction != (20, 0):
                direction = (-20, 0)

            if event.key == pygame.K_d and direction != (-20, 0):
                direction = (20, 0)
            if game_over and event.key == pygame.K_r:
             snake = [(300, 300), (280, 300), (260, 300)]
             direction = (20, 0)
             food = create_food()
             game_over = False
             game_started = True
             score = 0
            last_move_time = pygame.time.get_ticks()

    # Yılanın hareketi
    current_time = pygame.time.get_ticks()
    if not game_started:
       flicker = random.randint(1, 100) <= 3
    else:
       flicker = False

    blink_timer += clock.get_time()

    if blink_timer >= 500:
      show_prompt = not show_prompt
      blink_timer = 0
    

    if game_started and not game_over and current_time - last_move_time >= move_delay:

        head_x = snake[0][0] + direction[0]
        head_y = snake[0][1] + direction[1]

        new_head = (head_x, head_y)

        # Duvar çarpışması
        if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 600:
            game_over = True

        # Kendi gövdesine çarpma
        elif new_head in snake[:-1]:
            game_over = True

        if not game_over:
            snake.insert(0, new_head)

            # Yem yeme
            if snake[0] == food:
             score += 10
             food = create_food()
            else:
             snake.pop()

        last_move_time = current_time

    # Ekranı temizle
    game_surface.fill((5, 5, 8))
    glow_surface.fill((0, 0, 0, 0))
    if not game_started:
       for y in range(0, 600, 4):
        pygame.draw.line(
        game_surface,
        (50, 70,50),
        (0, y),
        (600, y)
)
        tape_text = title_font.render("TAPE DETECTED", True, (150, 150, 150))
        tape_rect = tape_text.get_rect(center=(300, 250))
        game_surface.blit(tape_text, tape_rect)

        # UNKNOWN
        date_text = small_font.render("RELEASE DATE: UNKNOWN", True, (85, 100, 85))
        date_rect = date_text.get_rect(center=(430, 50))
        game_surface.blit(date_text, date_rect)

        # PRESS SPACE TO PLAY
        play_text = title_font.render("PRESS SPACE TO PLAY", True, (100, 100, 100))
        play_rect = play_text.get_rect(center=(300, 350))

        if show_prompt:
            game_surface.blit(play_text, play_rect)

    # Yılanı çiz
    if game_started:
     for segment in snake:
        pygame.draw.circle(
    glow_surface,
    (0, 255, 100, 40),
    (segment[0] + 10, segment[1] + 10),
    25
)
        game_surface.blit(glow_surface, (0, 0))
        color = (255, 255, 255) if segment == snake[0] else (0, 255, 100)
        pygame.draw.rect(
            game_surface,
            color,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE),
            border_radius = 5
)

    # Yemi çiz
    pygame.draw.rect(
        game_surface,
        (255, 50, 50),
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
)

    # Game Over ekranı
    if game_over:
        text = font.render("GAME OVER", True, (255, 50, 50))

        final_score = font.render(f"Score: {score}", True, (255, 255, 255))
        final_score_rect = final_score.get_rect(center=(300, 364))
        game_surface.blit(final_score, final_score_rect)
        
        text_rect = text.get_rect(center=(300, 300))
        game_surface.blit(text, text_rect)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    game_surface.blit(score_text, (15, 15))

    vhs_surface.blit(game_surface, (0, 0))
    
    strip = vhs_surface.subsurface((0, 250, 600, 4)).copy()
    strip.scroll(5, 0)
    vhs_surface.blit(strip, (0, 200))
    screen.blit(vhs_surface, (0, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
