
import pygame
import random
import math

pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("20 Minutes Game")


hero_image = pygame.image.load("hero.png").convert_alpha()

monster_image = pygame.image.load("kiborg.png").convert_alpha()

background = pygame.image.load("background.png")



font = pygame.font.SysFont("Arial", 24)
lose = font.render('YOU LOSE', True, (188, 0, 0))


class Hero:
    def __init__(self, health, damage, x, y):
        self.health = health
        self.damage = damage
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(hero_image, (75, 75))
        self.speed = 5
        
    def move(self, keys):
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < height - self.image.get_height():
            self.y += self.speed
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < width - self.image.get_width():
            self.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Monster:
    def __init__(self, health, damage, x, y):
        self.health = health
        self.damage = damage
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(monster_image, (75, 75))
        self.speed = 2

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.speed = 10
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        self.dir_x = dx / dist
        self.dir_y = dy / dist
        self.radius = 5

    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius)

    def collide(self, monster):
        dist = math.hypot(monster.x - self.x, monster.y - self.y)
        return dist < 40

hero = Hero(health=100, damage=20, x=100, y=300)
monsters = [Monster(health=50, damage=10, x=random.randint(600, 780), y=random.randint(50, 550)) for _ in range(15)]
bullets = []

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            bullets.append(Bullet(hero.x + 32, hero.y + 32, mx, my))


    hero.move(keys)

    for monster in monsters:
        monster.move_towards(hero.x, hero.y)


    for bullet in bullets[:]:
        bullet.move()
        for monster in monsters[:]:
            if bullet.collide(monster):
                monster.health -= hero.damage
                if monster.health <= 0:
                    monsters.remove(monster)
                bullets.remove(bullet)
                break


    for monster in monsters:
        if math.hypot(monster.x - hero.x, monster.y - hero.y) < 40:
            hero.health -= monster.damage
            monsters.remove(monster)


    hero.draw(screen)
    for monster in monsters:
        monster.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)


    health_text = font.render(f"Health: {hero.health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)


    if hero.health <= 0:
        running = False
        screen.blit(lose, (300, 300))

pygame.quit()
