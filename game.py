import pygame
import random

pygame.init()

# स्क्रीन सेटअप
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Catching Game")

# रंग
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# खिलाड़ी (टोकरी)
player_width = 100
player_x = WIDTH // 2
player_y = HEIGHT - 40
player_speed = 10

# गेंद
ball_x = random.randint(0, WIDTH)
ball_y = 0
ball_speed = 5

score = 0

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # कीबोर्ड कंट्रोल
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # गेंद नीचे गिरना
    ball_y += ball_speed

    # गेंद रीसेट करना
    if ball_y > HEIGHT:
        ball_y = 0
        ball_x = random.randint(0, WIDTH)

    # टकराव (collision detection)
    if (ball_y + 20 >= player_y and
        player_x < ball_x < player_x + player_width):
        score += 1
        ball_y = 0
        ball_x = random.randint(0, WIDTH)

    # टोकरी बनाना
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, 20))

    # गेंद बनाना
    pygame.draw.circle(screen, RED, (ball_x, ball_y), 10)

    # स्कोर दिखाना
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()