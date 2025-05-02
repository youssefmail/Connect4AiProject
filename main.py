from game_logic import Game, State, RandomPlayer,  HumanPlayerByCommandLine, HumanPlayerByGUI
from game_ai import AiPlayer

# # To start game of human players
# g = Game([HumanPlayerByCommandLine("Alex"), HumanPlayerByCommandLine("Ali")])
# g.start_game()

# # To start game of random players
# g = Game([RandomPlayer("Random1"), RandomPlayer("Random2")])
# g.start_game()

# # To start game of human player vs random player
# g = Game([HumanPlayerByCommandLine("Ali"), RandomPlayer("random")])
# g.start_game()

# # To start game of human player vs ai player
# g = Game([HumanPlayerByCommandLine("Human"), AiPlayer()])
# g.start_game()

# To start game of human player vs ai player (WHY AI NOT CHOOSE ACTION 7 or 3 !! WHY CHOOSED ACTION 1 !!)
g = Game([HumanPlayerByCommandLine("Human"), AiPlayer()],init_state=State(actions_list=[
        2,
        3,
        2,
        2,
        3,
        0,
        2,
        3,
        4,
        3,
        4,
        3,
        3,
        4,
        5,
        5,
        5,
        0,
        0,
        # 0,
        # 2,
        # 6
    ]))
g.start_game()

# # To start game of human player vs ai player (WHY AI NOT CHOOSE ACTION 7 !! WHY CHOOSED ACTION 1 !!)
# g = Game([HumanPlayerByCommandLine("Human"), AiPlayer()],init_state=State(actions_list=[
#         3,
#         6,
#         3,
#         6,
#         3,
#         # 6,
#         # 3
#     ]))
# g.start_game()


# # To start game of ai player vs ai player
# g = Game([AiPlayer(), AiPlayer(level=4)])
# g.start_game()

# games recored at "games_history.json" to can retrive them
