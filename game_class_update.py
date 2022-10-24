import math
import random
import typing

import pygame
# from pygame import mixer

from Enemy import Enemy
from Bullet import Bullet

from menu import MainMenu
from scoreboard import Scoreboard

import time

# import json
import csv


class Game():
    def __init__(self):
        # Initialze the pygame
        pygame.init()
        self.running, self.playing = True, False
        # width, height
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        # Bg
        self.background = pygame.image.load('background.png')
        # Time
        self.init_time = time.time()
        # Platform
        self.platform = pygame.image.load('minus.png')
        self.platform_coordinates = [(300, 340),
                                     (364, 340),
                                     (428, 340),
                                     (40,  340),
                                     (104, 340),
                                     (650, 340),
                                     (714, 340),
                                     (220, 160),
                                     (284, 160),
                                     (344, 160),
                                     (600, 160),
                                     (664, 160)]

        # Caption and Icon
        pygame.display.set_caption("Watch Your Back")
        icon = pygame.image.load('handgun.png')
        pygame.display.set_icon(icon)

        # 0.18, 0.21
        self.global_speed = 0.23

        # Player
        # playerImg = pygame.image.load('gunman_right.png')
        self.playerImg = pygame.image.load('gunman_right.png')
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0
        self.playerY_change = 0
        self.playerX_speed = self.global_speed
        self.player_health = 3
        self.player_hit = False
        self.player_time_when_hit = 0
        self.player_direction = "right"
        self.player_jump = 0
        self.player_jump_down = False
        self.player_onplatformlayer = 0
        self.invincibility_frame = 2

        # Enemy
        self.number_of_enemies = 0
        self.max_number_of_enemies = 5
        self.index_of_enemy = 0
        self.enemies = []

        for i in range(self.max_number_of_enemies):
            e = Enemy(random.randint(0, 800), 480, self.global_speed * -
                      1.8, self.global_speed * -1.8, pygame.image.load('enemy_left.png'), "dead", i, 4, True)
            self.enemies.append(e)

        # Item Spawning
        self.hit_until_spawn = random.randint(10, 20)
        self.item_state = 'not spawned'
        self.itemX = 6900
        self.itemY = 6900
        self.time_when_get_item = 0
        print('hit until spawned = ' + str(self.hit_until_spawn))

        # Enemy Spawning
        self.spawn_points = [(-100, 280), (-100, 100), (-100, 480),
                             (900, 280), (900, 100), (900, 480)]
        self.spawn_time = time.time()
        self.spawn_rate = 1  # secs, 0.5
        self.increase_spawn_rate_time = time.time()

        # Bullet: Ready - can't see bullet, Fire - bullet is moving
        self.number_of_bullets = 10
        self.number_of_fired_bullets = 0
        self.bullets = []
        self.bullet_damage = 1

        # self, x, y, x_change, y_change, image, state, direction, index, time_when_shoot
        for i in range(self.number_of_bullets):
            b = Bullet(4200, 4200, self.global_speed * 10, 0,
                       pygame.image.load('bullet_right.png'), "ready", "right", i, 0)
            self.bullets.append(b)

        # score
        # dafont
        self.score_value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.textX = 10
        self.textY = 10

        # Game Over text
        self.over_font = pygame.font.Font('freesansbold.ttf', 64)

        self.scoreboard = []
        self.file_opened = False
        self.active = False
        self.min_score = 0

        self.base_font = pygame.font.Font(None, 32)
        self.user_text = ''
        self.input_rect = pygame.Rect(300, 450, 140, 32)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_passive

        for i in range(0, 5):
            # self.scoreboard.append(('None' + str(i), '0'))
            self.scoreboard.append({'name': 'None' + str(i), 'score': '0'})

        self.curr_scoreboard = Scoreboard(self)
        self.curr_menu = MainMenu(self)

    def reset_game(self):
        # Time
        self.init_time = time.time()
        # Player
        # playerImg = pygame.image.load('gunman_right.png')
        self.playerImg = pygame.image.load('gunman_right.png')
        self.playerX = 370
        self.playerY = 480
        self.playerX_change = 0
        self.playerY_change = 0
        self.playerX_speed = self.global_speed
        self.player_health = 5
        self.player_hit = False
        self.player_time_when_hit = 0
        self.player_direction = "right"
        self.player_jump = 0
        self.player_jump_down = False
        self.player_onplatformlayer = 0
        self.invincibility_frame = 2

        # Enemy
        self.number_of_enemies = 0
        self.max_number_of_enemies = 5
        self.index_of_enemy = 0
        self.enemies = []

        for i in range(self.max_number_of_enemies):
            e = Enemy(random.randint(0, 800), 480, self.global_speed * -
                      1.8, self.global_speed * -1.8, pygame.image.load('enemy_left.png'), "dead", i, 4, True)
            self.enemies.append(e)

        # Item Spawning
        self.hit_until_spawn = random.randint(10, 20)
        self.item_state = 'not spawned'
        self.itemX = 6900
        self.itemY = 6900
        self.time_when_get_item = 0

        # Enemy Spawning
        self.spawn_points = [(-100, 280), (-100, 100), (-100, 480),
                             (900, 280), (900, 100), (900, 480)]
        self.spawn_time = time.time()
        self.spawn_rate = 1  # secs
        self.increase_spawn_rate_time = time.time()

        # Bullet: Ready - can't see bullet, Fire - bullet is moving
        self.number_of_bullets = 10
        self.number_of_fired_bullets = 0
        self.bullets = []
        self.bullet_damage = 1

        # self, x, y, x_change, y_change, image, state, direction, index, time_when_shoot
        for i in range(self.number_of_bullets):
            b = Bullet(4200, 4200, self.global_speed * 10, 0,
                       pygame.image.load('bullet_right.png'), "ready", "right", i, 0)
            self.bullets.append(b)

        self.score_value = 0
        self.user_text = ''

    def show_score(self, x, y):
        score = self.font.render(
            "Score : " + str(self.score_value), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def game_over_text(self):
        over_text = self.over_font.render("GAME OVER", True, (255, 255, 255))
        # over_text = over_font.render("NICE", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))
        # go_back_text = self.font.render("press space to go back to the menu" + str(self.score_value), True, (255, 255, 255))
        # self.screen.blit(go_back_text, (100, 350))

    def init_platform(self):
        for coordinate in self.platform_coordinates:
            self.screen.blit(self.platform, coordinate)

    def player(self, x, y):
        # blit = draw
        self.screen.blit(self.playerImg, (x, y))

    def shoot(self):
        # global playerX, playerY, player_direction, number_of_fired_bullets

        self.bullet = self.bullets[self.number_of_fired_bullets]
        self.bullet.direction = self.player_direction
        if self.bullet.direction == "left":
            self.bullet.image = pygame.image.load("bullet_left.png")
        if self.bullet.direction == "right":
            self.bullet.image = pygame.image.load("bullet_right.png")

        self.bullet.x = self.playerX + 16
        self.bullet.y = self.playerY
        self.bullet.state = "fire"
        self.bullet.time_when_shoot = time.time()
        self.screen.blit(self.bullet.image, (self.bullet.x, self.bullet.y))
        self.number_of_fired_bullets = (self.number_of_fired_bullets + 1) % 10

    def jump_down(self):
        # global playerX, playerY, player_jump, player_jump_down, player_onplatformlayer

        self.player_jump_down = True
        # can't jump
        self.player_jump = 69

        # if playerY >= 480:
        #     player_jump_down = False
        #     player_jump = 0
        # else:
        #     for coordinate in platform_coordinates:
        #         if playerY >= coordinate[1] - 44 and playerY <= coordinate[1] - 34 and playerX >= coordinate[0] - 36 and playerX <= coordinate[1] + 36:
        #             if playerY

        if self.playerY >= 480:
            self.player_jump_down = False
            self.player_jump = 0
        elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 270 and self.playerX <= 462:
            self.player_onplatformlayer = 1
        elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 6 and self.playerX <= 138:
            self.player_onplatformlayer = 1
        elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 620 and self.playerX <= 748:
            self.player_onplatformlayer = 1
        elif self.playerY <= 116 + 10 and self.playerX >= 190 and self.playerX <= 374:
            self.player_onplatformlayer = 2
        elif self.playerY <= 116 + 10 and self.playerX >= 570 and self.playerX <= 694:
            self.player_onplatformlayer = 2

    def gravity(self):
        # global playerX, playerY, player_jump, player_jump_down, player_onplatformlayer, global_speed

        if self.playerY < 480:
            if self.player_jump_down:
                # falling, 0.7 with global speed 0.18 (global speed * 3.9)
                self.playerY += self.global_speed * 5
                if self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 270 and self.playerX <= 462 and self.player_onplatformlayer == 2:
                    self.player_jump_down = False
                    self.player_jump = 0
                    self.player_onplatformlayer = 1
                elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 6 and self.playerX <= 138 and self.player_onplatformlayer == 2:
                    self.player_jump_down = False
                    self.player_jump = 0
                    self.player_onplatformlayer = 1
                elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 620 and self.playerX <= 748 and self.player_onplatformlayer == 2:
                    self.player_jump_down = False
                    self.player_jump = 0
                    self.player_onplatformlayer = 1
                if self.playerY >= 480:
                    self.player_jump_down = False
                    self.playerY = 480
                    self.player_jump = 0
            elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 270 and self.playerX <= 462:
                if self.playerY_change == 0:
                    self.player_jump = 0
            elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 6 and self.playerX <= 138:
                if self.playerY_change == 0:
                    self.player_jump = 0
            elif self.playerY >= 296 and self.playerY <= 296 + 10 and self.playerX >= 620 and self.playerX <= 748:
                self.player_jump_down = False
                if self.playerY_change == 0:
                    self.player_jump = 0
            elif self.playerY >= 116 and self.playerY <= 116 + 10 and self.playerX >= 190 and self.playerX <= 374:
                if self.playerY_change == 0:
                    self.player_jump = 0
            elif self.playerY >= 116 and self.playerY <= 116 + 10 and self.playerX >= 570 and self.playerX <= 694:
                if self.playerY_change == 0:
                    self.player_jump = 0
            else:
                self.playerY += self.global_speed * 5
                if self.playerY >= 480:
                    self.player_jump_down = False
                    self.playerY = 480
                    self.player_jump = 0

    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface(
            (source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def spawn_an_enemy(self):
        # global spawn_time, spawn_rate, spawn_points, global_speed, enemies

        if time.time() - self.spawn_time >= self.spawn_rate:
            self.spawn_time = time.time()
            for enemy in self.enemies:
                # spawn one that was dead
                if enemy.state == "dead":
                    enemy.x = self.spawn_points[random.randint(0, 5)][0]
                    enemy.y = self.spawn_points[random.randint(0, 5)][1]
                    if enemy.x < 0:
                        enemy.x_change = self.global_speed * 1.8
                    if enemy.x > 800:
                        enemy.x_change = self.global_speed * -1.8

                    enemy.image = pygame.image.load('enemy_left.png')
                    enemy.state = "alive"
                    enemy.health = 4
                    enemy.just_spawned = True
                    break

    def isCollision(self, enemyX, enemyY, bulletX, bulletY):
        # finding distance with math
        distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                             math.pow(enemyY-bulletY, 2))
        if distance < 27:
            return True
        return False

    def handle_enemies(self):
        # global enemies, global_speed, bullets, score_value, playerX, playerY, player_health, player_time_when_hit, player_hit, playerImg

        for enemy in self.enemies:
            if enemy.health == 0 or enemy.state == "dead":
                continue

            enemy.x += enemy.x_change
            # enemy.y += enemy.y_change
            if enemy.just_spawned:
                if enemy.x >= 0 or enemy.x <= 736:
                    enemy.just_spawned = False
            else:
                if enemy.x <= 0:
                    enemy.image = pygame.image.load('enemy_right.png')
                    enemy.x_change = self.global_speed * 1.8
                if enemy.x >= 736:
                    enemy.image = pygame.image.load('enemy_left.png')
                    enemy.x_change = self.global_speed * -1.8
                if enemy.y <= 100:
                    enemy.y_change = self.global_speed * 1.8
                if enemy.y >= 480:
                    enemy.y_change = self.global_speed * -1.8

            # Collision
            collision = self.isCollision(
                enemy.x, enemy.y, self.playerX, self.playerY)
            if collision and time.time() - self.player_time_when_hit >= self.invincibility_frame:
                self.player_time_when_hit = time.time()
                self.player_hit = True
                self.player_health -= 1
                self.playerImg = pygame.image.load('gunman_dead.png')
                print("player_health = ", self.player_health)

            for bullet in self.bullets:
                collision = self.isCollision(
                    enemy.x, enemy.y, bullet.x, bullet.y)
                if collision:
                    # explosion_sound = mixer.Sound('explosion.wav')
                    bullet.y = 4200
                    bullet.state = "ready"
                    bullet.time_when_shoot = 0
                    if (enemy.x_change < 0 and bullet.direction == "left") or (enemy.x_change > 0 and bullet.direction == "right"):
                        # selling point: shot in the back deals more damage
                        # enemy.health -= 2
                        enemy.health -= self.bullet_damage * 2
                        if self.item_state == 'not spawned':
                            self.hit_until_spawn -= 1
                        print('hit in the back and self.hit_until_spawn = ' + str(self.hit_until_spawn))
                        print('item state = ' + str(self.item_state))
                        self.score_value += 2
                    else:
                        # enemy.health -= 1
                        enemy.health -= self.bullet_damage
                        self.score_value += 1

                    if enemy.health <= 0:
                        enemy.state = "dead"

                        if self.hit_until_spawn <= 0:
                            self.hit_until_spawn = random.randint(10, 20)
                            print('new hit until spawned = ' + str(self.hit_until_spawn))
                            self.item_state = 'spawned'
                            self.itemX = enemy.x
                            self.itemY = enemy.y
                            print('itemX and itemY = ' + str(self.itemX) + ', ' + str(self.itemY))
                        continue

            # enemy(enemy) # type error, fix later
            self.screen.blit(enemy.image, (enemy.x, enemy.y))

    def handle_bullets(self):
        # global bullets, global_speed

        for bullet in self.bullets:
            if bullet.x < 0:
                bullet.x = 800
            if bullet.x > 800:
                bullet.x = 0

            if time.time() - bullet.time_when_shoot >= self.global_speed * 2.5 and bullet.time_when_shoot != 0:
                bullet.time_when_shoot = 0
                bullet.x = -69
                bullet.state = "ready"

            if bullet.state == "fire":
                self.screen.blit(bullet.image, (bullet.x + 16, bullet.y + 0))
                if bullet.direction == "right":
                    bullet.x += bullet.x_change
                if bullet.direction == "left":
                    bullet.x -= bullet.x_change

    # def isCollision(enemyX, enemyY, bulletX, bulletY):
    #     # finding distance with math
    #     distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
    #                          math.pow(enemyY-bulletY, 2))
    #     if distance < 27:
    #         return True
    #     return False

    def get_score(self, e):
        return int(e['score']) * -1

    def game_loop(self):
        # running = True
        while self.playing:
            # rgb
            self.screen.fill((192, 192, 192))
            if self.item_state == 'power up acquired':
                self.screen.fill((192, 128, 128))
            # bg (heavy)
            # screen.blit(background, (0, 0))
            # Platform
            self.init_platform()

            if self.player_health <= 0:
                self.playerImg = pygame.image.load('gunman_dead.png')
                self.player(self.playerX, self.playerY)

                for enemy in self.enemies:
                    enemy.y = 2000

                self.game_over_text()
                self.show_score(self.textX, self.textY)
                # pygame.display.update()

                # old_scores = [0, 0, 0, 0, 0]
                # self.min_score = 0

                if not self.file_opened:
                    try:
                        index = 1

                        with open("scoreboard.csv", 'r') as file:
                            csvreader = csv.reader(file)
                            header = next(csvreader)
                            # self.scoreboard[0] = (header[0], header[1])
                            self.scoreboard[0] = {
                                'name': header[0], 'score': header[1]}
                            # old_scores.append(header[1])

                            for count, row in enumerate(csvreader):
                                if count % 2 != 0:
                                    # self.scoreboard[index] = (
                                    # row[0], row[1])
                                    self.scoreboard[index] = {
                                        'name': row[0], 'score': row[1]}
                                    # old_scores[index] = row[1]
                                    index += 1

                            self.min_score = min(int(self.scoreboard[0]['score']), int(self.scoreboard[1]['score']),
                                                 int(self.scoreboard[2]['score']), int(self.scoreboard[3]['score']), int(self.scoreboard[4]['score']))
                    except:
                        self.min_score = 0
                        print('No file created yet')

                    # print('min_score = ' + str(min_score))
                    # print('self.score_value = ' + str(self.score_value))
                    print('self.scoreboard = ' + str(self.scoreboard))
                    self.file_opened = True

                if self.score_value > self.min_score:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.playing = False
                            self.running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.input_rect.collidepoint(event.pos):
                                self.active = True
                            else:
                                self.active = False
                        if event.type == pygame.KEYDOWN:
                            if self.active:
                                if event.key == pygame.K_BACKSPACE:
                                    # 0 to -1 (last one)
                                    self.user_text = self.user_text[:-1]
                                else:
                                    self.user_text += event.unicode
                            if event.key == pygame.K_RETURN:
                                self.user_text = self.user_text[:-1]
                                self.scoreboard.append(
                                    {'name': self.user_text, 'score': str(self.score_value)})
                                print(self.scoreboard)
                                # File "c:\Users\ASUS\Desktop\Game Assignment\game_class_update.py", line 484, in game_loop
                                #     self.scoreboard.sort(key=self.get_score)
                                # TypeError: get_score() takes 1 positional argument but 2 were given
                                self.scoreboard.sort(key=self.get_score)

                                with open('scoreboard.csv', mode='w') as scoreboard:
                                    scoreboard_writer = csv.writer(
                                        scoreboard, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                                    for i in range(0, 5):
                                        scoreboard_writer.writerow(
                                            [self.scoreboard[i]['name'], self.scoreboard[i]['score']])

                                self.file_opened = False
                                self.playing = False

                    if self.active:
                        color = self.color_active
                    else:
                        color = self.color_passive

                    pygame.draw.rect(self.screen, color, self.input_rect, 2)

                    text_surface = self.base_font.render(
                        self.user_text, True, (255, 255, 255))
                    self.screen.blit(
                        text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

                    self.input_rect.w = max(text_surface.get_width() + 10, 200)

                    self.gravity()
                    pygame.display.update()
                    continue

                self.gravity()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.playing = False
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            self.playing = False
                        if event.key == pygame.K_r:
                            self.reset_game()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False

                # KEYDOWN = pressed keystroke
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.playerImg = pygame.image.load('gunman_left.png')
                        self.playerX_change = self.playerX_speed * -4
                        self.player_direction = "left"

                    if event.key == pygame.K_RIGHT:
                        self.playerImg = pygame.image.load('gunman_right.png')
                        self.playerX_change = self.playerX_speed * 4
                        self.player_direction = "right"

                    if event.key == pygame.K_SPACE:
                        self.shoot()

                    if event.key == pygame.K_UP:
                        # double jump
                        if self.player_jump < 2:
                            # 13
                            self.playerY_change = self.global_speed * -12
                            self.player_jump += 1

                    if event.key == pygame.K_DOWN:
                        self.jump_down()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                        self.playerX_change = 0

            # player movement
            self.playerX += self.playerX_change
            if self.playerY_change < 0:
                self.playerY += self.playerY_change
                self.playerY_change += 0.01
                if self.playerY_change >= 0:
                    self.playerY_change = 0

            # gravity
            self.gravity()

            # selling point of this game: teleportation at screen's end
            if self.playerX <= 0:
                self.playerX = 735
            if self.playerX >= 736:
                self.playerX = 0

            # Spawning
            self.spawn_an_enemy()

            # Handling enemies
            self.handle_enemies()

            # Item Spawning
            if self.item_state == 'spawned':
                self.screen.blit(pygame.image.load(
                    'power.png'), (self.itemX, self.itemY))
                if self.isCollision(
                        self.itemX, self.itemY, self.playerX, self.playerY):
                    print('player power up')
                    self.item_state = 'power up acquired'
                    self.time_when_get_item = time.time()
                    # self.playerX_change *= 4
                    self.playerX_speed *= 1.5
                    self.bullet_damage += 3

            if time.time() - self.time_when_get_item >= 5 and self.time_when_get_item != 0:
                print('player back to normal')
                self.item_state = 'not spawned'
                self.time_when_get_item = 0
                # self.playerX_change /= 4
                self.playerX_speed /= 1.5
                self.bullet_damage -= 3

            # Bullet Movement
            self.handle_bullets()

            # Increasing Difficulty
            if time.time() - self.increase_spawn_rate_time >= 20 and self.spawn_rate > 0.2:
                self.increase_spawn_rate_time = time.time()
                self.spawn_rate -= 0.1
                print('20 sec interval spawn rate = ' + str(self.spawn_rate) + ' sec')

            if time.time() - self.init_time >= 40 and self.max_number_of_enemies < 10:
                self.init_time = time.time()
                e = Enemy(random.randint(0, 800), 480, self.global_speed * -
                      1.8, self.global_speed * -1.8, pygame.image.load('enemy_left.png'), "dead", self.max_number_of_enemies, 4, True)
                self.enemies.append(e)
                self.max_number_of_enemies += 1
                self.spawn_rate += 0.1
                print('40 sec interval max enemy = ' + str(self.max_number_of_enemies))
                print('40 sec interval spawn rate = ' + str(self.spawn_rate))

            # if self.score_value >= 420 or self.player_health <= 0:
            #     self.playerImg = pygame.image.load('gunman_dead.png')
            #     self.playerX -= self.playerX_change
            #     self.playerY -= self.playerY_change

            #     for enemy in self.enemies:
            #         enemy.y = 2000
            #     self.game_over_text()

            # if time.time() - player_time_when_hit <= invincibility_frame/4 or (time.time() - player_time_when_hit <= invincibility_frame*3/4 and time.time() - player_time_when_hit > invincibility_frame/2):
            if time.time() - self.player_time_when_hit <= self.invincibility_frame/8 or (time.time() - self.player_time_when_hit <= self.invincibility_frame*3/8 and time.time() - self.player_time_when_hit > self.invincibility_frame*2/8) or (time.time() - self.player_time_when_hit <= self.invincibility_frame*5/8 and time.time() - self.player_time_when_hit > self.invincibility_frame*4/8) or (time.time() - self.player_time_when_hit <= self.invincibility_frame*7/8 and time.time() - self.player_time_when_hit > self.invincibility_frame*6/8):
                self.blit_alpha(self.screen, self.playerImg,
                                (self.playerX, self.playerY), 64)
            else:
                self.player(self.playerX, self.playerY)
            self.show_score(self.textX, self.textY)
            pygame.display.update()
