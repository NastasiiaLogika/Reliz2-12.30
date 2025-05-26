from pygame import*

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")
background = transform.scale(image.load("background.jpeg"), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, player_images, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_images), (65, 65))
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
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
            
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
            

run = True
clock = time.Clock()
while run:
    window.blit(background, (0,0))
    
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    display.update()
    clock.tick(60)
            
    