import math
import random

import pygame
# from pygame import mixer

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

global_speed = 0.1

# Player
# playerImg = pygame.image.load('gunman_right.png')
playerImg = pygame.image.load('gunman_right.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0
player_direction = "right"

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 3

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('enemy_left.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(480)
    enemyX_change.append(global_speed * -3)
    enemyY_change.append(0)

# Bullet: Ready - can't see bullet, Fire - bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = -69
bulletY = 480
bulletX_change = global_speed * 10
bullet_state = "ready"
bullet_direction = "right"

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


def enemy(x, y, i):
    # blit = draw
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 0))


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
                if bullet_state == "ready":
                    # bullet_sound = mixer.Sound('laser.wav')
                    # bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bullet_direction = player_direction
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    # selling point of this game: teleportation at screen's end
    if playerX <= 0:
        # playerX = 0
        playerX = 735
    if playerX >= 736:
        # playerX = 736
        playerX = 0

    for i in range(number_of_enemies):
        # Game Over
        if enemyY[i] < 200:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyImg[i] = pygame.image.load('enemy_right.png')
            enemyX_change[i] = global_speed * 3
        if enemyX[i] >= 736:
            enemyImg[i] = pygame.image.load('enemy_left.png')
            enemyX_change[i] = global_speed * -3

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explosion_sound = mixer.Sound('explosion.wav')
            bulletX = -69
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletX < 0 or bulletX > 800:
        bulletX = -69
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        if bullet_direction == "right":
            bulletX += bulletX_change
        if bullet_direction == "left":
            bulletX -= bulletX_change

    if score_value == 69:
        for j in range(number_of_enemies):
                enemyY[j] = 2000
        game_over_text()
        
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
