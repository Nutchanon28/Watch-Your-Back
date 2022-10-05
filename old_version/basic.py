import math
import random

import pygame
# from pygame import mixer

from Enemy import Enemy
from Bullet import Bullet

import time

# Initialze the pygame
pygame.init()

# width, height
screen = pygame.display.set_mode((800, 600))
# screen = pygame.display.set_mode((919, 1149))

# Bg
background = pygame.image.load('background.png')
# background = pygame.image.load('the_messiah.jpg')

# Background Sound, -1 for playing on loop for some reason
# mixer.music.load('background.wav')
# mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Watch Your Back")
icon = pygame.image.load('handgun.png')
pygame.display.set_icon(icon)

global_speed = 0.2

# Player
# playerImg = pygame.image.load('gunman_right.png')
playerImg = pygame.image.load('gunman_right.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
player_direction = "right"

# Enemy
number_of_enemies = 3
enemies = []

for i in range(number_of_enemies):
    e = Enemy(random.randint(0, 800), 480, global_speed * -
              2, 0, pygame.image.load('enemy_left.png'))
    enemies.append(e)

# Bullet: Ready - can't see bullet, Fire - bullet is moving
number_of_bullets = 10
number_of_fired_bullets = 0
bullets = []

# self, x, y, x_change, y_change, image, state, direction, index, time_when_shoot
for i in range(number_of_bullets):
    b = Bullet(-69, 480, global_speed * 10, 0,
               pygame.image.load('bullet_right.png'), "ready", "right", i, 0)
    bullets.append(b)


# score
# dafont
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    # over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    over_text = over_font.render("NICE", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    # blit = draw
    screen.blit(playerImg, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # finding distance with math
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    return False


running = True
while running:
    # rgb
    screen.fill((192, 192, 192))
    # print is log

    # bg (heavy)
    # screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # KEYDOWN = pressed keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # playerImg = pygame.image.load('gunman_left.png')
                playerImg = pygame.image.load('gunman_left.png')
                playerX_change = global_speed * -4
                player_direction = "left"
            if event.key == pygame.K_RIGHT:
                # playerImg = pygame.image.load('gunman_right.png')
                playerImg = pygame.image.load('gunman_right.png')
                playerX_change = global_speed * 4
                player_direction = "right"
            if event.key == pygame.K_SPACE:
                bullet = bullets[number_of_fired_bullets]
                bullet.direction = player_direction
                if bullet.direction == "left":
                    bullet.image = pygame.image.load("bullet_left.png")
                if bullet.direction == "right":
                    bullet.image = pygame.image.load("bullet_right.png")

                bullet.x = playerX
                bullet.state = "fire"
                bullet.time_when_shoot = time.time()
                screen.blit(bullet.image, (bullet.x + 16, playerY + 0))
                number_of_fired_bullets = (number_of_fired_bullets + 1) % 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # selling point of this game: teleportation at screen's end
    if playerX <= 0:
        playerX = 735
    if playerX >= 736:
        playerX = 0

    for enemy in enemies:
        enemy.x += enemy.x_change
        if enemy.x <= 0:
            enemy.image = pygame.image.load('enemy_right.png')  
            enemy.x_change = global_speed * 2
        if enemy.x >= 736:
            enemy.image = pygame.image.load('enemy_left.png')
            enemy.x_change = global_speed * -2

        # Collision
        # for bullet in bullets:
        # collision = isCollision(enemy.x, enemy.y, bullet.x, bullet.y)
        bulletY = 480
        for bullet in bullets:
            collision = isCollision(enemy.x, enemy.y, bullet.x, bullet.y)
            if collision:
                # explosion_sound = mixer.Sound('explosion.wav')
                bulletX = -69
                bullet_state = "ready"

                bullet.x = -69
                bullet.state = "ready"
                bullet.time_when_shoot = 0
                score_value += 1
                enemy.x = random.randint(0, 800)

        # enemy(enemy) # type error, fix later
        screen.blit(enemy.image, (enemy.x, enemy.y))

    # Bullet Movement
    for bullet in bullets:
        # if bullet.x < 0 or bullet.x > 800:
        #     bullet.x = -69
        #     bullet.state = "ready"

        if bullet.x < 0:
            bullet.x = 800
        if bullet.x > 800:
            bullet.x = 0

        if time.time() - bullet.time_when_shoot >= global_speed * 2 and bullet.time_when_shoot != 0:
            # print(str(global_speed * 2) + " seconds passed")
            bullet.time_when_shoot = 0
            bullet.x = -69
            bullet.state = "ready"

        if bullet.state == "fire":
            screen.blit(bullet.image, (bullet.x + 16, playerY + 0))
            if bullet.direction == "right":
                bullet.x += bullet.x_change
            if bullet.direction == "left":
                bullet.x -= bullet.x_change

    if score_value == 69:
        for enemy in enemies:
            enemy.y = 2000
        game_over_text()

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
