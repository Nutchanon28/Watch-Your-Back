import pygame
# from menu import MainMenu

import json
import csv

class Scoreboard():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.display = pygame.Surface(
            (self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.window = pygame.display.set_mode(
            (self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.run_display = False
        self.player_names = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5']
        # self.player_names = [{'name' : 'None0', 'score' : '0'}, {'name' : 'None0', 'score' : '0'}, {'name' : 'None0', 'score' : '0'}, {'name' : 'None0', 'score' : '0'}, {'name' : 'None0', 'score' : '0'}]

        try:
            # with open('scoreboard.csv', 'r') as csv_file:
            #     csv_reader = csv.reader(csv_file, delimiter=',')
            #     line_count = 0
            #     for row in csv_reader:
            #         if line_count == 0:
            #             line_count += 1
            #             continue

            #         line_count += 1
            #         self.player_names[row - 1] = row[0] + ' : ' + row[1]
            #         print(str(self.player_names))
                index = 1

                with open("scoreboard.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    header = next(csvreader)
                    self.player_names[0] = header[0] + ' : ' + header[1]

                    for count, row in enumerate(csvreader):
                        if count % 2 != 0:
                            self.player_names[index] = row[0] + ' : ' + row[1]
                            index += 1
        except:
            print('No file created yet')

        # self.curr_menu = MainMenu(self)
        print(str(self.player_names))


    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def display_scoreboard(self):
        try:
            index = 1
            with open("scoreboard.csv", 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                self.player_names[0] = header[0] + ' : ' + header[1]

                for count, row in enumerate(csvreader):
                    if count % 2 != 0:
                        self.player_names[index] = row[0] + ' : ' + row[1]
                        index += 1
        except:
            print('No file created yet')

        while self.run_display:
            self.display.fill((0, 0, 0))
            for i in range(0, 5):
                self.draw_text(self.player_names[i], 20, self.mid_w, self.mid_h - 100 + i * 50)
            self.draw_text("65010290 Nutchanon Mongkonvilas", 18, self.game.DISPLAY_W - 200, self.game.DISPLAY_H - 100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_display = False
                    self.game.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.run_display = False

            self.blit_screen()
