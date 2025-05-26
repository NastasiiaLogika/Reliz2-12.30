from pygame import*
from random import*
from time import time as timer

win_width = 800
win_height = 600

display.set_caption('Shooter')
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
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

img_bullet = "bullet.png"
bullets = sprite.Group()

ship = Player("rocket.png", 5, win_height - 100, 100, 120, 10)

img_enemy = "enemy.png"
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80),
                    -40, 80, 50, randint(1,5))
    monsters.add(monster)


font.init()
font2 = font.Font(None, 36)

run = True
finish = False
rel_time = False
num_fire = 0
score = 0
lost = 0
goal = 10
max_lost = 3
life = 3

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
        
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        ship.update()
        ship.reset()
        
        monsters.update()
        monsters.draw(window)
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
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
            
        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life = life - 1
        
        
        if life == 0 or lost >= max_lost:
            finish = True
            window(lost, (200, 200))
            
        if score >= goal:
            finish = True
            window(score, (200, 200))
            
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = font2.render("Життя: " + str(life), 1, life_color)
        window.blit(text_life, (450, 10))
        
        
        display.update()
    time.delay(50)       
            
    