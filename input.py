                # scores = [0, 0, 0, 0, 0]
                # try:
                #     index = 1

                #     with open("scoreboard.csv", 'r') as file:
                #         csvreader = csv.reader(file)
                #         header = next(csvreader)
                #         # self.player_names[0] = header[0] + \
                #         # ' : ' + header[1]
                #         self.scoreboard[0] = (header[0], header[1])

                #         for count, row in enumerate(csvreader):
                #             if count % 2 != 0:
                #                 # self.player_names[index] = row[0] + \
                #                 # ' : ' + row[1]
                #                 self.scoreboard[index] = (
                #                     row[0], row[1])
                #                 scores[index] = row[1]
                #                 index += 1
                # except:
                #     print('No file created yet')

                # if max(scores[0], scores[1], scores[2], scores[3], scores[4], self.score_value) == self.score_value:
                #     input_rect = pygame.Rect(200, 200, 140, 32)
                #     color = pygame.Color('lightskyblue3')

                #     for event in pygame.event.get():
                #         if event.type == pygame.KEYDOWN:
                #             if event.key == pygame.K_BACKSPACE:
                #                 user_text = user_text[:-1]
                #             elif event.key == pygame.K_RETURN:
                #                 with open('scoreboard.csv', mode='w') as scoreboard:
                #                     scoreboard_writer = csv.writer(
                #                         scoreboard, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                #                     for i in range(0, 5):
                #                         # scoreboard_writer.writerow(
                #                         # [self.scoreboard[i][0], self.scoreboard[i][1]])
                #                         scoreboard_writer.writerow(
                #                             [self.scoreboard[i][0], str(self.score_value)])

                #                 self.playing = False
                #             else:
                #                 user_text += event.unicode

                #     pygame.draw.rect(self.screen, color, input_rect, 2)

                #     base_font = pygame.font.Font(
                #         'freesansbold.ttf', 32)

                #     text_surface = base_font.render(
                #         user_text, True, (255, 255, 255))
                #     self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

                #     input_rect.w = max(text_surface.get_width(), 200)