from pygame import*
from random import*

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
        self.rect_x = player_x
        self.rect_y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        pass


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y =  0
            lost = lost + 1


ship = Player("rocket.png", 5, win_height - 100, 80, 100, 10)


img_enemy = 'enemy.png'
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80),
                    -40, 80, 50, randint(1, 5))
    monsters.add(monster)



run = True
finish = False
while run:
    window.blit(bagckround, (0,0))
    
    for e in event.get():
        if e.type == QUIT:
            run = False


    if not finish:
        window.blit(bagckround, (0, 0))


        for e in event.get():
            if e.type == QUIT:
                run == False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 5 and real_time == False:
                        num_fire = num_fire + 1
                        ship.fire()

        ship.update()
        ship.reset()

        monsters.update()
        monsters.draw(window)

        display.update()
    time.delay(50)