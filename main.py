from game_logic import *
from game_ai import AiPlayer

# # To start game of Two human player
# g = Game([HumanPlayerByCommandLine("Alex"), HumanPlayerByCommandLine("Ali")])
# g.start_game()

# To start game of random player vs human player
g = Game([HumanPlayerByCommandLine("Ali"), AiPlayer()])
g.start_game()

# # To start game of random player
# g = Game([RandomPlayer("Random1"), RandomPlayer("Random2")])
# g.start_game()

# games recored at "games.csv" to can retrive them