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

# Platform
platform = pygame.image.load('minus.png')

# Background Sound, -1 for playing on loop for some reason
# mixer.music.load('background.wav')
# mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Watch Your Back")
icon = pygame.image.load('handgun.png')
pygame.display.set_icon(icon)

global_speed = 0.18

# Player
# playerImg = pygame.image.load('gunman_right.png')
playerImg = pygame.image.load('gunman_right.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
player_direction = "right"
player_jump = 0
player_jump_down = False
player_onplatformlayer = 0

# Enemy
number_of_enemies = 1
max_number_of_enemies = 5
enemies = []

for i in range(number_of_enemies):
    e = Enemy(random.randint(0, 800), 480, global_speed * -
              1.8, global_speed * -1.8, pygame.image.load('enemy_left.png'), 3)
    enemies.append(e)

# Enemy Spawning
spawn_points = [(100, 280), (100, 100), (100, 480), (700, 280), (700, 100), (700, 480)]
spawn_time = time.time()
spawn_rate = 2  # secs

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
    # Platform
    screen.blit(platform, (300, 340))
    screen.blit(platform, (364, 340))
    screen.blit(platform, (428, 340))

    screen.blit(platform, (40, 340))
    screen.blit(platform, (104, 340))

    screen.blit(platform, (650, 340))
    screen.blit(platform, (714, 340))

    screen.blit(platform, (220, 160))
    screen.blit(platform, (284, 160))
    screen.blit(platform, (344, 160))

    screen.blit(platform, (600, 160))
    screen.blit(platform, (664, 160))

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

                bullet.x = playerX + 16
                bullet.y = playerY
                bullet.state = "fire"
                bullet.time_when_shoot = time.time()
                screen.blit(bullet.image, (bullet.x, bullet.y))
                number_of_fired_bullets = (number_of_fired_bullets + 1) % 10
            if event.key == pygame.K_UP:
                if player_jump < 2:
                    playerY_change = global_speed * -13
                    player_jump += 1
            if event.key == pygame.K_DOWN:
                player_jump_down = True
                player_jump = 69

                if playerY >= 480:
                    player_jump_down = False
                    player_jump = 0
                elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 270 and playerX <= 462:
                    player_onplatformlayer = 1
                elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 6 and playerX <= 138:
                    player_onplatformlayer = 1
                elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 620 and playerX <= 748:
                    player_onplatformlayer = 1
                elif playerY >= 116 and playerY <= 116 + 10 and playerX >= 190 and playerX <= 374:
                    player_onplatformlayer = 2
                elif playerY >= 116 and playerY <= 116 + 10 and playerX >= 570 and playerX <= 694:
                    player_onplatformlayer = 2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerY_change < 0:
        playerY += playerY_change
        playerY_change += 0.01
        if playerY_change >= 0:
            playerY_change = 0
    # gravity
    if playerY < 480:
        if player_jump_down:
            # falling
            playerY += 0.7
            if playerY >= 296 and playerY <= 296 + 10 and playerX >= 270 and playerX <= 462 and player_onplatformlayer == 2:
                player_jump_down = False
                player_jump = 0
                player_onplatformlayer = 1
            elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 6 and playerX <= 138 and player_onplatformlayer == 2:
                player_jump_down = False
                player_jump = 0
                player_onplatformlayer = 1
            elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 620 and playerX <= 748 and player_onplatformlayer == 2:
                player_jump_down = False
                player_jump = 0
                player_onplatformlayer = 1
            if playerY >= 480:
                player_jump_down = False
                playerY = 480
                player_jump = 0
        elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 270 and playerX <= 462:
            if playerY_change == 0:
                player_jump = 0
        elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 6 and playerX <= 138:
            if playerY_change == 0:
                player_jump = 0
        elif playerY >= 296 and playerY <= 296 + 10 and playerX >= 620 and playerX <= 748:
            player_jump_down = False
            if playerY_change == 0:
                player_jump = 0
        elif playerY >= 116 and playerY <= 116 + 10 and playerX >= 190 and playerX <= 374:
            if playerY_change == 0:
                player_jump = 0
        elif playerY >= 116 and playerY <= 116 + 10 and playerX >= 570 and playerX <= 694:
            if playerY_change == 0:
                player_jump = 0
        else:
            playerY += 0.7
            if playerY >= 480:
                player_jump_down = False
                playerY = 480
                player_jump = 0

    # selling point of this game: teleportation at screen's end
    if playerX <= 0:
        playerX = 735
    if playerX >= 736:
        playerX = 0

    # Spawning
    if time.time() - spawn_time >= spawn_rate and number_of_enemies <= max_number_of_enemies:
        spawn_time = time.time()
        e = Enemy(spawn_points[random.randint(0, 5)][0], spawn_points[random.randint(0, 5)][1], global_speed * -
                  1.8, global_speed * -1.8, pygame.image.load('enemy_left.png'), 3)
        enemies.append(e)
        number_of_enemies += 1

    enemy_dying = 0
    for enemy in enemies:
        if enemy.health == 0:
            continue

        enemy.x += enemy.x_change
        # enemy.y += enemy.y_change
        if enemy.x <= 0:
            enemy.image = pygame.image.load('enemy_right.png')
            enemy.x_change = global_speed * 1.8
        if enemy.x >= 736:
            enemy.image = pygame.image.load('enemy_left.png')
            enemy.x_change = global_speed * -1.8
        if enemy.y <= 100:
            enemy.y_change = global_speed * 1.8
        if enemy.y >= 480:
            enemy.y_change = global_speed * -1.8

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
                enemy.health -= 1
                if enemy.health <= 0:
                    enemy_dying += 1
                    continue

        # enemy(enemy) # type error, fix later
        screen.blit(enemy.image, (enemy.x, enemy.y))
    number_of_enemies -= enemy_dying

    # Bullet Movement
    for bullet in bullets:
        # if bullet.x < 0 or bullet.x > 800:
        #     bullet.x = -69
        #     bullet.state = "ready"

        if bullet.x < 0:
            bullet.x = 800
        if bullet.x > 800:
            bullet.x = 0

        if time.time() - bullet.time_when_shoot >= global_speed * 2.5 and bullet.time_when_shoot != 0:
            # print(str(global_speed * 2) + " seconds passed")
            bullet.time_when_shoot = 0
            bullet.x = -69
            bullet.state = "ready"

        if bullet.state == "fire":
            screen.blit(bullet.image, (bullet.x + 16, bullet.y + 0))
            if bullet.direction == "right":
                bullet.x += bullet.x_change
            if bullet.direction == "left":
                bullet.x -= bullet.x_change

    if score_value == 420:
        for enemy in enemies:
            enemy.y = 2000
        game_over_text()

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
