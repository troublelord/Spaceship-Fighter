import pygame
import sys
import random


    
pygame.init()

window = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()

class Sprite:
    pass

def display_sprite(sprite):
    window.blit(sprite.image, (sprite.x, sprite.y))

font = pygame.font.Font(None, 24)
foreground = (200, 200, 200)

background = (0, 0, 0)
ship_image = pygame.image.load("fighter.png")

ship_destroyed = pygame.image.load("ship_destroyed.png")
bullet_image = pygame.image.load("bullet.png")
alien_image = pygame.image.load("alien.png")

ship = Sprite()
ship.x = 0
ship.y = 0
ship.image = ship_image

score = 0
lives = 3
bullets = []
aliens = []
stars = []
frames_until_next_alien = random.randrange(30, 100)
frames_until_next_star = 0

def add_star():
    star = Sprite()
    star.x = window.get_width()
    star.y = random.randrange(10, window.get_height() - 10)
    star.size = random.randrange(1, 4)
    star.image = pygame.Surface((star.size, star.size))
    star.image.fill((255, 255, 255))
    stars.append(star)

def get_sprite_rectangle(sprite):
    return sprite.image.get_rect().move(sprite.x, sprite.y)

def fire_bullet():
    bullet = Sprite()
    bullet.x = ship.x + 125
    bullet.y = ship.y + 65
    bullet.used = False
    bullet.image = bullet_image
    bullets.append(bullet)

def add_alien():
    alien = Sprite()
    alien.x = window.get_width()
    alien.y = random.randrange(100, window.get_height() - 100)
    alien.image = alien_image
    aliens.append(alien)
    alien.hit = False

def init():
    global frames_until_next_star
    frames_until_next_star = frames_until_next_star - 1
    if frames_until_next_star <= 0:
        frames_until_next_star = random.randrange(10, 30)
        add_star()
        
    for star in stars:        
        star.x = star.x - 2


for i in range(500):
    init()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_bullet()
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_ESCAPE]:
        sys.exit()
    
    if lives>0:
        if pressed_keys[pygame.K_UP]:
            ship.y = ship.y - 8

        if pressed_keys[pygame.K_DOWN]:
            ship.y = ship.y + 8

        if pressed_keys[pygame.K_LEFT]:
            ship.x = ship.x - 8
        
        if pressed_keys[pygame.K_RIGHT]:
            ship.x = ship.x + 8

        if ship.y < 0:
            ship.y = 0

        if ship.y > window.get_height() - ship_image.get_height()  :
            ship.y = window.get_height() - ship_image.get_height()

        if ship.x < 0:
            ship.x = 0

        if ship.x > window.get_width() - ship_image.get_width() :
            ship.x = window.get_width() - ship_image.get_width()


    for bullet in bullets:
        bullet.x = bullet.x + 15

    bullets = [bullet for bullet in bullets if bullet.x < window.get_width() and not bullet.used]

    

    frames_until_next_alien = frames_until_next_alien - 1
    if frames_until_next_alien <= 0 and lives>0:
        frames_until_next_alien = 50
        add_alien()

    for alien in aliens:
        alien.x = alien.x - 3

    aliens = [alien for alien in aliens if alien.x > - alien_image.get_width() and not alien.hit]

    frames_until_next_star = frames_until_next_star - 1
    if frames_until_next_star <= 0:
        frames_until_next_star = random.randrange(10, 30)
        add_star()

    for star in stars:
        
        star.x = star.x - 2

    stars = [star for star in stars if star.x > - 10]

    
    ship_rect = get_sprite_rectangle(ship)

    for alien in aliens:
        alien_rect = get_sprite_rectangle(alien)
        if alien_rect.colliderect(ship_rect) and lives > 0:
            alien.hit = True
            alien.x = alien.x - 6
            alien.y = alien.y - 6
            lives = lives - 1            
            continue
        
        for bullet in bullets:
            if alien_rect.colliderect(get_sprite_rectangle(bullet)):
                alien.hit = True
                bullet.used = True
                score = score + 10
                continue


    window.fill(background)    

    for star in stars:
        display_sprite(star)
        if star.size == 1:
            star.x = star.x + 1
        elif star.size == 2:
            star.x = star.x + 0.5
   
        
    display_sprite(ship)


    for bullet in bullets:
        if lives > 0:
            display_sprite(bullet)

    for alien in aliens:
        
            display_sprite(alien)

    if lives == 0:
         ship.image = ship_destroyed
         if ship.x > -500:
             ship.x = ship.x - 6
         gameover = font.render("GAME OVER!!!" , 1, foreground)
         gameover_pos = score_text.get_rect()
         gameover_pos.right = window.get_width()/2
         gameover_pos.top = window.get_height()/2
         window.blit(gameover, gameover_pos)
         

    score_text = font.render("SCORE: " + str(score), 1, foreground)
    score_text_pos = score_text.get_rect()
    score_text_pos.right = window.get_width() - 10
    score_text_pos.top = 10
    window.blit(score_text, score_text_pos)
    lives_text = font.render("LIVES: " + str(lives), 1, foreground)
    window.blit(lives_text, (10, 10))
    pygame.display.flip()
    

    clock.tick(50)
