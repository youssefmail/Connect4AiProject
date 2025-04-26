from game_logic import *
from game_ai import *
from game_ai_debug import *

# # To start game of Two human player
# g = Game([HumanPlayerByCommandLine("Alex"), HumanPlayerByCommandLine("Ali")])
# g.start_game()

# To start game of random player vs human player
g = Game([AiPlayer2(1,4,"Ai player1"), AiPlayer2(2,3,"AI player2")])
g.start_game()

# # To start game of random player
# g = Game([RandomPlayer("Random1"), RandomPlayer("Random2")])
# g.start_game()

# games recored at "games.csv" to can retrive them