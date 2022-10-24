# from game_testing import Game
from game_class_update import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.reset_game()  
    g.game_loop()
    g.curr_scoreboard.display_scoreboard()