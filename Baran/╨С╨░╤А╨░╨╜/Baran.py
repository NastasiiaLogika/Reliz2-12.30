import pygame
import random
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Runer")

WHITE = (255, 255, 255)
GREEN = (0, 102, 0)
RED = (255, 0, 0)

player_size = 50
player_x  = screen_width // 2
player_y = screen_height - 2 * player_size
player_speed = 10

obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacle_list = []

score = 0

font = pygame.font.SysFont("monospace", 35)

# Функція для створення нових перешкод
def create_obstacle():
    x_pos = random.randint(0, screen_width - obstacle_width)
    y_pos = 0 - obstacle_height
    obstacle_list.append([x_pos, y_pos])

# Функція для оновлення позиції перешкод
def update_obstacles():
    global score
    for obstacle in obstacle_list:
        obstacle[1] += obstacle_speed
        if obstacle[1] > screen_height:  
            obstacle_list.remove(obstacle)
            score += 1 

# Функція для перевірки зіткнень
def check_collisions():
    for obstacle in obstacle_list:
        if (player_x < obstacle[0] < player_x + player_size or player_x < obstacle[0] 
            + obstacle_width < player_x + player_size) and (player_y < obstacle[1] < player_y 
                                                            + player_size or player_y < obstacle[1] 
                                                            + obstacle_height < player_y + player_size):
            return True
    return False

# Основний цикл гри
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False 

    keys = pygame.key.get_pressed()

    # Рухаємо гравця залежно від натиснутих клавіш
    if keys[pygame.K_LEFT] and player_x - player_speed >= 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_speed <= screen_width - player_size:
        player_x += player_speed

    if random.randint(1, 20) == 1:  
        create_obstacle()

    update_obstacles()

    if check_collisions():
        running = False 


    screen.fill(WHITE)


    pygame.draw.circle(screen, GREEN, (player_x + player_size // 2, player_y + player_size // 2), player_size // 2)

    
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], obstacle_width, obstacle_height))

    # Відображаємо рахунок
    score_text = font.render("Рахунок: {}".format(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Оновлюємо екран
    pygame.display.flip()

    # Встановлюємо частоту оновлення екрану
    pygame.time.Clock().tick(30)

# Виходимо з Pygame
pygame.quit()
sys.exit()