import pygame
import random

pygame.init()
pygame.mixer.init()

# Розміри вікна
Width = 800
Height = 500
win = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Minecraft 2D")

# Кольори
bg_color = (0, 130, 240)
Platform_color = (100, 50, 20)
Platform2_color = (0, 255, 120)
sun_color = (255, 255, 0)

# Гравець
player_width = 50
player_height = 100
player_x = 350
player_y = 300
player_vel = 5
jump_power = 12
gravity = 0.5
velocity_y = 0
on_ground = False

# Звук
hit_sound = pygame.mixer.Sound("hit.mp3")
lvl_sound = pygame.mixer.Sound("lvl.mp3")
zombie_sound = pygame.mixer.Sound("zombie.mp3")
dead_sound = pygame.mixer.Sound("dead.mp3")
eat_sound = pygame.mixer.Sound("eat.mp3")
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
hit_sound.set_volume(1.0)
lvl_sound.set_volume(1.0)
eat_sound.set_volume(1.0)


# Зображення
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_hp = 10
player_alive = True

# Платформи
platform_rect = pygame.Rect(0, 400, 800, 100)
platform2_rect = pygame.Rect(0, 400, 800, 20)

# Сонце
sun_rect = pygame.Rect(0, 0, 100, 100)

# Свиня
pig_img = pygame.image.load("pig.png")
pig_img = pygame.transform.scale(pig_img, (50, 50))
pig_rect = pygame.Rect(random.randint(50, 500), 350, 50, 50)
pig_hp = 5
pig_alive = True
pig_velocity_y = 0
pig_gravity = 0.5
pig_escape_dir = 0  
pig_escape_timer = 0
pig_move_timer = 0  

# Зомбі
zombie_img = pygame.image.load("zombie.png")
zombie_img = pygame.transform.scale(zombie_img, (50, 50))
zombie_rect = pygame.Rect(random.randint(50, 500), 350, 50, 50)
zombie_hp = 5
zombie_alive = True
zombie_velocity_y = 0
zombie_gravity = 0.5
zombie_escape_dir = 0  
zombie_escape_timer = 0
zombie_move_timer = 0  



# Блоки
block1_img = pygame.image.load("Grass.png")
block1_img = pygame.transform.scale(block1_img, (50, 50))
block2_img = pygame.image.load("Dirt.png")
block2_img = pygame.transform.scale(block2_img, (50, 50))
block3_img = pygame.image.load("Stone.png")
block3_img = pygame.transform.scale(block3_img, (50, 50))
block4_img = pygame.image.load("Wood.jpg")
block4_img = pygame.transform.scale(block4_img, (50, 50))
block5_img = pygame.image.load("Wood2.png")
block5_img = pygame.transform.scale(block5_img, (50, 50))
block6_img = pygame.image.load("Door.jpg")
block6_img = pygame.transform.scale(block6_img, (50, 100))

B1_img = pygame.transform.scale(block1_img, (25, 25))
B2_img = pygame.transform.scale(block2_img, (25, 25))
B3_img = pygame.transform.scale(block3_img, (25, 25))
B4_img = pygame.transform.scale(block4_img, (25, 25))
B5_img = pygame.transform.scale(block5_img, (25, 25))
B6_img = pygame.transform.scale(block6_img, (25, 50))

blocks = []
block_types = [block1_img, block2_img, block3_img, block4_img, block5_img, block6_img]
current_block = 0

# Головний цикл
running = True
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Вдарити або видалити блок
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if pig_alive and pig_rect.collidepoint(mouse_x, mouse_y):
                hit_sound.play()
                pig_hp -= 1
                pig_velocity_y = -8  # Підстрибування

               
                if player_rect.centerx < pig_rect.centerx:
                    pig_escape_dir = 1
                else:
                    pig_escape_dir = -1

                pig_escape_timer = 30
                pig_move_timer = random.randint(20, 60)  # таймер для випадкових рухів

                if pig_hp <= 0:
                    pig_alive = False
                    lvl_sound.play()
                    pig_escape_dir = 0

            if zombie_alive and zombie_rect.collidepoint(mouse_x, mouse_y):
                hit_sound.play()
                zombie_sound.play()
                zombie_hp -= 1
                zombie_velocity_y = -8  # Підстрибування

                # Напрям втечі
                if player_rect.centerx < zombie_rect.centerx:
                    zombie_escape_dir = 1
                else:
                    zombie_escape_dir = -1

                zombie_escape_timer = 30
                zombie_move_timer = random.randint(20, 60)  # таймер для випадкових рухів

                if zombie_hp <= 0:
                    zombie_alive = False
                    dead_sound.play()
                    lvl_sound.play()
                    zombie_escape_dir = 0
                
                

            # Видалення блоку
            for block in blocks[:]:
                if block[0] <= mouse_x < block[0] + 50 and block[1] <= mouse_y < block[1] + 50:
                    blocks.remove(block)
                    break

        # Додати блок
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            block_x = (mouse_x // 50) * 50
            block_y = (mouse_y // 50) * 50
            blocks.append((block_x, block_y, block_types[current_block]))

        # Вибір блоку
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_block = 0
            elif event.key == pygame.K_2: current_block = 1
            elif event.key == pygame.K_3: current_block = 2
            elif event.key == pygame.K_4: current_block = 3
            elif event.key == pygame.K_5: current_block = 4
            elif event.key == pygame.K_6: current_block = 5

    # Рух гравця
    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_a]:
        dx = -player_vel
    if keys[pygame.K_d]:
        dx = player_vel

    player_rect.x += dx

    if keys[pygame.K_e]:
        eat_sound.play()
   
    

    

    # Колізії (горизонтально)
    for block in blocks:
        block_height = 100 if block[2] == block6_img else 50
        block_rect = pygame.Rect(block[0], block[1], 50, block_height)
        if player_rect.colliderect(block_rect):
            if dx > 0: player_rect.right = block_rect.left
            elif dx < 0: player_rect.left = block_rect.right

    # Стрибок
    if keys[pygame.K_SPACE] and on_ground:
        velocity_y = -jump_power
        on_ground = False

    # Гравітація гравця
    velocity_y += gravity
    player_rect.y += int(velocity_y)
    on_ground = False

    if player_rect.colliderect(platform_rect):
        if velocity_y > 0:
            player_rect.y = platform_rect.y - player_height
            velocity_y = 0
            on_ground = True

    # Колізії (вертикально)
    for block in blocks:
        block_height = 100 if block[2] == block6_img else 50
        block_rect = pygame.Rect(block[0], block[1], 50, block_height)
        if player_rect.colliderect(block_rect):
            if velocity_y > 0:
                player_rect.bottom = block_rect.top
                velocity_y = 0
                on_ground = True
            elif velocity_y < 0:
                player_rect.top = block_rect.bottom
                velocity_y = 0

    # Свиня: гравітація, втеча і випадкові рухи
    if pig_alive:
        pig_velocity_y += pig_gravity
        pig_rect.y += int(pig_velocity_y)

        if pig_rect.y >= 350:
            pig_rect.y = 350
            pig_velocity_y = 0

        if pig_escape_timer > 0:
            pig_rect.x += pig_escape_dir * 4
            pig_escape_timer -= 1

            if pig_rect.left < 0:
                pig_rect.left = 0
            if pig_rect.right > Width:
                pig_rect.right = Width

        if pig_move_timer > 0:
            pig_move_timer -= 1
        elif pig_move_timer == 0:
            pig_escape_dir = random.choice([-1, 1])  # випадковий напрямок руху
            pig_move_timer = random.randint(20, 60)  # новий таймер для руху

    
    if zombie_alive:
        zombie_velocity_y += zombie_gravity
        zombie_rect.y += int(zombie_velocity_y)

        if zombie_rect.y >= 350:
            zombie_rect.y = 350
            zombie_velocity_y = 0

        if zombie_escape_timer > 0:
            zombie_rect.x += zombie_escape_dir * 4
            zombie_escape_timer -= 1

            if zombie_rect.left < 0:
                zombie_rect.left = 0
            if zombie_rect.right > Width:
                zombie_rect.right = Width

        if zombie_move_timer > 0:
            zombie_move_timer -= 1
        elif zombie_move_timer == 0:
            zombie_escape_dir = random.choice([-1, 1])  # випадковий напрямок руху
            zombie_move_timer = random.randint(20, 60)  # новий таймер для руху

    # Малювання
    win.fill(bg_color)
    win.blit(player_img, (player_rect.x, player_rect.y))
    pygame.draw.rect(win, Platform_color, platform_rect)
    pygame.draw.rect(win, Platform2_color, platform2_rect)
    pygame.draw.rect(win, sun_color, sun_rect)

    # Панель блоків
    win.blit(B1_img, (300, 450))
    win.blit(B2_img, (335, 450))
    win.blit(B3_img, (370, 450))
    win.blit(B4_img, (405, 450))
    win.blit(B5_img, (440, 450))
    win.blit(B6_img, (475, 440))

    # Блоки
    for block in blocks:
        win.blit(block[2], (block[0], block[1]))

    # Свиня
    if pig_alive:
        win.blit(pig_img, (pig_rect.x, pig_rect.y))
        font = pygame.font.SysFont(None, 24)
        hp_text = font.render(f"HP: {pig_hp}", True, (0, 0, 0))
        win.blit(hp_text, (pig_rect.x, pig_rect.y - 20))

    # Зомбі
    if zombie_alive:
        win.blit(zombie_img, (zombie_rect.x, zombie_rect.y))
        font = pygame.font.SysFont(None, 24)
        zombie_HP = font.render(f"HP: {zombie_hp}", True, (0, 0, 0))
        win.blit(zombie_HP, (zombie_rect.x, zombie_rect.y - 20))

   
    if player_alive:
        font = pygame.font.SysFont(None, 24)
        player_HP = font.render(f"HP: {player_hp}", True, (0, 0, 0))
        win.blit(player_HP, (player_rect.x, player_rect.y - 20))




    pygame.display.update()

pygame.quit()
