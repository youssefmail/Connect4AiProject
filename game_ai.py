from game_logic import *


class AiPlayer:
    def __init__(self, player=2, level=1, name="Ai Player"):
        if player not in (1, 2):
            raise ValueError("Player must be either 1 or 2")
        self.name = name
        self.player = player
        self.level = level
        self.depth = level + 1
        self.rows = 6
        self.cols = 7

    def get_default_name(self):
        return "Ai Player"

    def get_player_action(self, state):
        maximizing = (self.player == 1)
        _, action = self._minimax(self.depth, maximizing, state,alpha=float('-inf'), beta=float('inf'))
        return action


    def _minimax(self, depth, is_maximizing, state, alpha, beta):
        if state.isTerminated() or depth == 0:
            score = self._evaluate(state)
            return score, None

        actions = state.get_available_actions()
        if not actions:
            score = self._evaluate(state)
            return score, None

        best_action = None

        if is_maximizing:
            best_score = float('-inf')
            for action in actions:
                new_state = state.take_action_in_different_state_object(action, self.player)  # AI's move
                score, _ = self._minimax(depth - 1, False, new_state, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_action = action
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  
        else:
            best_score = float('inf')
            for action in actions:
                new_state = state.take_action_in_different_state_object(action, 3 - self.player)  # Opponent's move
                score, _ = self._minimax(depth - 1, True, new_state, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_action = action
                beta = min(beta, score)
                if beta <= alpha:
                    break  

        return best_score, best_action

    def _evaluate(self, state):
        # Terminal states
        if state.isTerminated():
            winner = state.get_winner_number()
            if winner == self.player:
                return float('inf')
            elif winner == 0:
                return 0
            else:
                return float('-inf')

        board = state._table
        score = 0
        # Center column preference
        center_col = self.cols // 2
        center_count = sum(1 for r in range(self.rows) if board[r][center_col] == self.player)
        score += center_count * 3

        # Score all windows of length 4
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
                # positive diagonal
                window = [board[r + i][c + i] for i in range(4)]
                score += self._score_window(window)
                # negative diagonal
                window = [board[r + 3 - i][c + i] for i in range(4)]
                score += self._score_window(window)

        return score

    def _score_window(self, window):
        
        score = 0
        opp = 3 - self.player
        count_self = window.count(self.player)
        count_opp = window.count(opp)
        count_empty = window.count(0)

        if count_self == 4:
            score += 100
        elif count_self == 3 and count_empty == 1:
            score += 5
        elif count_self == 2 and count_empty == 2:
            score += 2

        if count_opp == 3 and count_empty == 1:
            score -= 4

        return score



# Notes:
# - This evaluation uses sliding windows of length 4 across rows, columns, and diagonals.
# - Center column control is weighted as +3 per piece.
# - Terminal wins/losses are handled with infinite scores for clarity.
# - Original specialized 2/3 in-row functions have been unified into _score_window.
# TODO:
# - Consider weighting lower rows higher (distance from bottom)
# - Explore fork opportunities and more advanced heuristics
# - use alpha beta algorithm