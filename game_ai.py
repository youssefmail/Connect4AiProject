from game_logic import *

class AiPlayer:
    
    def __init__ (self, player = 2, level = 1):
        if player not in (1, 2):
            raise ValueError("Player must be either 1 or 2")

        self.player = player
        self.level = level
        self.depth = level + 1
        self.rows = 6
        self.cols = 7
    

    def _eval(self, state):
        board = state._table
        
        try:
            # check winning 
            if state.get_winner_number() == 0:
                return 0
            elif state.get_winner_number() == 1:
                return -100
            elif state.get_winner_number() == 2:
                return 100
        except Exception as e:
            pass

        rating = 0
        


        
    
    def _evaluate_3_in_row(self, board):
        #player_1_count = 0
        #player_2_count = 0
        prev_player = 0
        count = 0
        result = [0,0]

        # Check horizontaly
        for row in range(self.rows):
            for col in range(self.cols):
                player = board[row][col]

                if player == 0:
                    count = 0
                    prev_player = 0
                elif player == prev_player:
                    count += 1
                elif player != prev_player:
                    count = 1
                    prev_player = player


                if count == 3 and col == self.cols -1:
                    if board[row][col-3] == 0 :
                        result[player-1] += 12
                    else:
                        result[player-1] += 8 
                elif count == 3 and col != self.cols -1:
                    if board[row][col-3] == 0 or board[row][col+1] == 0 :
                        result[player-1] += 15 
                    else:
                        result[player-1] += 10
                
        count = 0
        return result

        # Check vertically


    def get_available_columns(self, board):
        result = []
        for col in range(len(board[0])):
            if col == 0:
                result.append(col + 1)

        return result
    


# testing
player = AiPlayer()

board = [
    [0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 0, 0, 0, 0, 0],  
    [0, 0, 1, 0, 0, 0, 0],  
    [0, 0, 1, 0, 2, 2, 2],  
    [0, 2, 1, 1, 1, 2, 2]   
]
print(player._evaluate_3_in_row(board))

# +15  3 in row middle have zero before or after
# +10  3 in row middle
# +12  3 in row edges have zero before or after
# +8  3 in row edges
# +6  2 in row middle
# +3  2 in row edges