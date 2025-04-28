from game_logic import Game, State, RandomPlayer,  HumanPlayerByCommandLine, HumanPlayerByGUI
from game_ai import *

# # To start game of human players
# g = Game([HumanPlayerByCommandLine("Alex"), HumanPlayerByCommandLine("Ali")])
# g.start_game()

# # Test game_logic has no errors
# for i in range(1000):
#     g = Game([RandomPlayer("random1"), RandomPlayer("random2")])
#     g.start_game()

# # To start game of random players
# g = Game([RandomPlayer("Random1"), RandomPlayer("Random2")])
# g.start_game()

# # To start game of human player vs random player
# g = Game([HumanPlayerByCommandLine("Ali"), RandomPlayer("random")])
# g.start_game()

# To start game of human player vs ai player
g = Game([HumanPlayerByCommandLine("Human"), AiPlayer(2, "Ai player")])
g.start_game()

# # To start game of ai player vs ai player
# g = Game([AiPlayer(1, "Ai player 1"), AiPlayer(2, "Ai player 2",level=4)])
# g.start_game()

# games recored at "games_history.json" to can retrive them
