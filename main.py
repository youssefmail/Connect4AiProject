from game_logic import Game, State, RandomPlayer,  HumanPlayerByCommandLine, HumanPlayerByGUI
from game_ai import AiPlayer

# # Gui program
# from game_gui import start_gui
# if __name__ == "__main__":
#     start_gui()


# from game_logic import Game, State, RandomPlayer,  HumanPlayerByCommandLine, HumanPlayerByGUI
# from game_ai import AiPlayer

# # # To start game of human players
# # g = Game([HumanPlayerByCommandLine("Alex"), HumanPlayerByCommandLine("Ali")])
# # g.start_game()
# # Gui program

# # # To start game of random players
# # g = Game([RandomPlayer("Random1"), RandomPlayer("Random2")])
# # g.start_game()

# To start game of human player vs random player
g = Game([HumanPlayerByCommandLine("Human"), AiPlayer(name="Ai player")])
g.start_game()

# # # To start game of ai player vs ai player
# # g = Game([AiPlayer(), AiPlayer(level=4)])
# # g.start_game()

# # games recored at "games_history.json" to can retrive them