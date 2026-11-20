
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Coin Collector")

player_x = 100
player_y = 100
player_size = 40
coin_x = 400
coin_y = 300
coin_radius = 15

running = True

while running:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_y -= 5

    if keys[pygame.K_s]:
        player_y += 5

    if keys[pygame.K_a]:
        player_x -= 5

    if keys[pygame.K_d]:
        player_x += 5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    pygame.draw.rect(
        screen,
        (0, 100, 255),
        (player_x, player_y, player_size, player_size)
    )
    pygame.draw.circle(
        screen, (255,215,0), (coin_x,coin_y), coin_radius)

    pygame.display.flip()

pygame.quit()
