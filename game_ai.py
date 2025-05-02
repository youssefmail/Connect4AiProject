from game_logic import State, ComputerPlayer


class AiPlayer(ComputerPlayer):
    def __init__(self, level=2, name="Ai Player"):
        self.name = name
        self.my_player_number = None # will be known after first get_player_action() call
        self.level = level
        self.depth = level + 2
        self.rows = 6
        self.cols = 7

    def get_player_action(self, state):
        self.my_player_number = state.get_who_player_turn()
        _, action = self._minimax(self.depth, True, state, alpha=float('-inf'), beta=float('inf'))
        return action

    def _minimax(self, depth, is_maximizing, state, alpha=float("-inf"), beta=float("inf")):
        # return best_score, best_action
     
        # alpha is best value for max player
        # beta is best value for min player

        if depth == 0:
            value = self._evaluate(state)
            return value, None 

        if state.is_terminate():
            value = self._evaluate(state)
            return value, None 

        actions = state.get_available_actions()
        if not actions:
            value = self._evaluate(state)
            return value, None 
        

        best_action = None

        if is_maximizing:
            best_value = float('-inf')
            for action in actions:
                new_state = state.take_action_in_different_state_object(action)
                value, _ = self._minimax(depth - 1, False, new_state, alpha, beta)


                if value > best_value or best_action is None:
                    best_value = value
                    best_action = action
                if value >= beta:
                    break # returns best_value
                if value > alpha:
                    alpha = value
                
        else:
            best_value = float('inf')
            for action in actions:
                new_state = state.take_action_in_different_state_object(action)
                value, _  = self._minimax(depth - 1, True, new_state, alpha, beta)


                if value < best_value or best_action is None:
                    best_value = value
                    best_action = action
                if value <= alpha:
                    break # returns best_value
                if value < beta:
                    beta = value

        return best_value, best_action 

    def _evaluate(self, state):
        if state.is_terminate():
            winner = state.get_winner_player_number()
            if winner == self.my_player_number:
                return float('inf')
            elif winner == 0:
                return 0
            else:
                return float('-inf')

        board = state.get_board_as_list() # same as state._table
        score = 0
        
        center_preference = [0, 1, 2, 3, 2, 1, 0]  
        for col in range(self.cols):
            col_count = sum(1 for r in range(self.rows) if board[r][col] == self.my_player_number)
            score += col_count * center_preference[col] * 3

        for r in range(self.rows):
            for c in range(self.cols - 3):
                window = [board[r][c + i] for i in range(4)]
                score += self._score_window(window)

        for c in range(self.cols):
            for r in range(self.rows - 3):
                window = [board[r + i][c] for i in range(4)]
                score += self._score_window(window)

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self._score_window(window)

                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self._score_window(window)


        return score

    def _score_window(self, window):
        score = 0
        opp = 3 - self.my_player_number
        count_self = window.count(self.my_player_number)
        count_opp = window.count(opp)
        count_empty = window.count(0)


        if count_self == 3 and count_empty == 1:
            score += 10
        elif count_self == 2 and count_empty == 2:
            score += 4

        if count_opp == 3 and count_empty == 1:
            score -= 20
        elif count_opp == 2 and count_empty == 2:
            score -= 4

        return score