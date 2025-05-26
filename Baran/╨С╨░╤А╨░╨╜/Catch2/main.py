from pygame import*

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Лабіринт")
background = transform.scale(image.load("background.jpeg"), (win_width, win_height))

class GameSprite(sprite.Sprite):
    #конструктор класу
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
            

##################################################          
class Enemy(GameSprite):
    direction = "left"
    
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"
        
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed  
            
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_widht = wall_width
        self.wall_height = wall_height
        self.image = Surface((self.wall_widht, self.wall_height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
            
x1 = 100
y1 = 300

x2 = 300
y2 = 300

player = Player('sprite1.png', 5, 420, 4)
monster = Enemy('sprite2.png', 620, 280, 2)
final = GameSprite('treasure.png', 580, 420, 0)

w1 = Wall(154, 205, 50, 80, 480, 600, 10)#верхня
w6 = Wall(154, 205, 50, 80, 20, 600, 10)#нижня

w2 = Wall(154, 205, 50, 80, 360, 150, 10)
w3 = Wall(154, 205, 50, 200, 250, 150, 10)

w4 = Wall(154, 205, 50, 280, 150, 100, 10)
w5 = Wall(154, 205, 50, 450, 120, 120, 10)

w10 = Wall(154, 205, 50, 80, 20, 10, 340)
w12 = Wall(154,205, 50, 680, 20, 10, 470)
w11 = Wall(154, 205, 50, 450, 120, 10, 370)

w7 = Wall(154, 205, 50, 350, 250, 10, 240)
w9 = Wall(154, 205, 50, 200, 150, 10, 100)
w8 = Wall(154, 205, 50, 280, 150, 10, 100)
#################################################

run = True
clock = time.Clock()
#################################################
finish = False
#################################################
while run:
    window.blit(background, (0,0))
    
    for e in event.get():
        if e.type == QUIT:
            run = False
            
    #############################################        
    if finish != True:   
        window.blit(background, (0,0))    
        player.reset()
        monster.reset()
        final.reset()
        player.update()
        monster.update()
        
        w1.draw_wall()
        w6.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w10.draw_wall()
        w12.draw_wall()
        w11.draw_wall()
        w7.draw_wall()
        w8.draw_wall()
        w9.draw_wall()
            
    
    player.reset()
    monster.reset()
    ############################################
    
    display.update()
    clock.tick(60)
            
    