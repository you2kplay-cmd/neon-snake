
import pygame
import random

pygame.init()
pygame.font.init()

# Pencere ayarları
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Neon Snake")
clock = pygame.time.Clock()

# Yazı tipi
font = pygame.font.SysFont("Arial", 50, bold=True)

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
score = 0

glow_surface = pygame.Surface((600, 600), pygame.SRCALPHA)
# Ana oyun döngüsü
while running:

    # Olayları kontrol et
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

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

    # Yılanın hareketi
    current_time = pygame.time.get_ticks()

    if not game_over and current_time - last_move_time >= move_delay:

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
    screen.fill((5, 5, 8))
    glow_surface.fill((0, 0, 0, 0))

    # Yılanı çiz
    for segment in snake:
        pygame.draw.circle(
    glow_surface,
    (0, 255, 100, 40),
    (segment[0] + 10, segment[1] + 10),
    25
)
        color = (255, 255, 255) if segment == snake[0] else (0, 255, 100)
        pygame.draw.rect(
            screen,
            color,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE),
            border_radius = 5
)

    # Yemi çiz
    pygame.draw.rect(
        screen,
        (255, 50, 50),
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
)

    # Game Over ekranı
    if game_over:
        text = font.render("GAME OVER", True, (255, 50, 50))

        final_score = font.render(f"Score: {score}", True, (255, 255, 255))
        final_score_rect = final_score.get_rect(center=(300, 364))
        screen.blit(final_score, final_score_rect)
        
        text_rect = text.get_rect(center=(300, 300))
        screen.blit(text, text_rect)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (15, 15))
    screen.blit(glow_surface, (0, 0))
    
    for segment in snake:
     color = (255, 255, 255) if segment == snake[0] else (0, 255, 100)
     pygame.draw.rect(
        screen,
        color,
        (segment[0], segment[1], CELL_SIZE, CELL_SIZE),
        border_radius=5
    )
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
