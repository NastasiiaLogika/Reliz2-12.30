from pygame import*
from random import*
from time import time as timer

win_width = 800
win_height = 600

display.set_caption(' . ')
window = display.set_mode((win_width, win_height))
bagckround = transform.scale(image.load("background.png"), (win_width, win_height))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y)
        )
        self.speed = player_speed
        
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed
    def fire(self):
        bullet = bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
    

    

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
        
        if self.rect.y > win_height:
            self.rect.x = randint(190, win_width - 80)
            self.rect.y = randint(190, win_height - 80)
            self.speed = randint(4, 8)

class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -40
            self.speed = randint(4, 8)
            
            


img_bullet = "bullet.png"
bullets = sprite.Group()

ship = Player("player.png", 5, win_height - 100, 100, 120, 10)

img_enemy = "enemy.png"
monsters1 = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(40, win_width - 80),
                    -40, 80, 50, randint(1,5))
    monsters1.add(monster)

img_enemy1 = "enemy1.png"
monsters2 = sprite.Group()
for y in range(1, 6):
    monster = Enemy1(img_enemy, randint(80, win_width - 80),
                    -40, 80, 50, randint(4,8))
    monsters2.add(monster)


font.init()
font2 = font.Font(None, 36)
font3 = font.Font(None, 86)

run = True
start_ticks = time.get_ticks()
finish = False
rel_time = False
num_fire = 0
score = 0
lost = 0
goal = 25
max_lost = 3
life = 3
level = 1

def GameRestart():
    Enemy.kill(monsters1)
    Enemy1.kill(monsters2)
    ship.reset()
    monsters1.update()
    monsters2.update()
    ship.update()

while run:
    window.blit(bagckround, (0,0))
    
    for e in event.get():
        if e.type == QUIT:
                        run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    ship.fire()
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True
        
    if not finish:
        window.blit(bagckround, (0,0))
        keys = key.get_pressed()


        seconds = (time.get_ticks() - start_ticks) // 1000


        timer_text = font2.render("Рахунок: " + str(seconds) + " сек", True, (255, 255, 255))
        window.blit(timer_text, (10, 50))

        ship.update()
        ship.reset()
        
        monsters1.update()
        monsters1.draw(window)
        monsters2.update()
        monsters2.draw(window)
        bullets.update()  
        bullets.draw(window)
        
        
        #перезарядка
        if rel_time == True:
            now_time = timer()
            
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        
        collides = sprite.groupcollide(monsters1, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 50, randint(4,8))
            monsters1.add(monster)
            
        collides = sprite.groupcollide(monsters2, bullets, True, True)
        for c in collides:
            score = score + 1
            monsters2.add(monster)

        hits1 = sprite.spritecollide(ship, monsters1, True)  # Видаляє ворогів з групи monsters1
        hits2 = sprite.spritecollide(ship, monsters2, True)  # Видаляє ворогів з групи monsters2

        if hits1 or hits2:
                life -= 1

                monster.kill()
            
        if keys[K_r]:
            GameRestart()

        if life == 0:
            finish = True
            lose = font3.render("Програв!", 1, (180, 0, 0))
            window.blit(lose, (300, 250))

            

            
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = font2.render("Життя: " + str(life), 1, life_color)
        window.blit(text_life, (450, 10))
        
        if seconds >= 25:
            level = level + 1
            goal = goal + 20
            for m in monsters2:
                m.speed += 0.5


            level_show_start_time = time.get_ticks()  # зберігаємо момент початку показу



        if level == 2:
            level_text = font3.render("Level 2", 1, (255, 255, 0))
            window.blit(level_text, (300, 300))
        if seconds >= 45:
            level = level + 1
            goal = goal + 20
            for m in monsters2:
                m.speed += 0.5
            level_show_start_time = time.get_ticks()
        if level == 3:
            level_text = font3.render("Level 3", 1, (255, 255, 0))
            window.blit(level_text, (300, 300)) 
        if seconds >= 60:
            win = font3.render("Перемога!!!", 1, (0, 180, 0))
            finish = True
            window.blit(win, (300, 250))
            
            
        display.update()
    time.delay(50)       