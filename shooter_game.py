#Создай собственный Шутер!

from pygame import *
from random import randint
from time import sleep

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 35, self.rect.y, 15, 20, 15)
        global bullets
        bullets.add(bullet)

lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(80,620)
            lost += 1

class Star(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(0, win_width)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), 0, 80, 50, randint(1, 5))
    monsters.add(monster)
stars = sprite.Group()

for i in range(30):
    star = Star('star.png', randint(0, win_width), randint(0, win_height), 5, 5, randint(2, 6))
    stars.add(star)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 36)

run = True
finish = False

clock = time.Clock()
FPS = 60
score = 0
live = 5

rel_time = False
num_fire = 0
from time import time as timer

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire > 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if rel_time:
        if timer() - last_time >= 3:
            rel_time = False
            num_fire = 0

    if finish == False:
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))

        window.blit(background,(0,0))
        window.blit(text_lose, (10, 20))

        text = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 60))

        text_live = font1.render('Жизни:'+ str(live), True, (255, 255, 255))
        window.blit(text_live, (10, 100))

        ship.update()
        monsters.update()
        stars.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        stars.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), 0, 80, 50, randint(1, 5))
            monsters.add(monster)

        if score >= 10:
            finish = True
            win = font1.render('YOU WIN!', True, (255, 255, 255))
            window.blit(win, (200, 200))

        for asteroid in sprite.spritecollide(ship, asteroids, False):
            live -= 1
            asteroid.rect.y = -asteroid.rect.height
            asteroid.rect.x = randint(0, win_width - asteroid.rect.width)

        for monster in sprite.spritecollide(ship, monsters, False):
            live -= 1
            monster.rect.y = -monster.rect.height
            monster.rect.x = randint(0, win_width - monster.rect.width)

        if sprite.spritecollide(ship, monsters, True):
            live -= 1

        if lost >= 3 or live <= 0:
            finish = True
            lose = font1.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(lose, (200, 200))

        display.update()

    else:
        finish = False
        score = 0 
        lost = 0
        live = 5
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        sleep(5)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        ship.rect.y = win_height - 100
        ship.rect.x = win_width // 2
    
    time.delay(FPS)

    print('hello world')