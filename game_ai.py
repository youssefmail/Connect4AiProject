from game_logic import *
from abc import ABC, abstractmethod

class AiPlayer:
    
    def __init__ (self, player = 2, level = 1, name = "Aiplayer"):
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
        if self.player == 2:
            best_action = self.minimax(self.depth, False, state)[1]
        else:
            best_action = self.minimax(self.depth, True, state)[1]

        return best_action

    def minimax(self, depth, is_maximizing, state):
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
                score, _ = self.minimax(depth - 1, False, new_state)
                if score > best_score:
                    best_score = score
                    best_action = action
        else:

            best_score = float('inf')
            for action in actions:
                new_state = state.take_action_in_different_state_object(action, 3 - self.player)  # Opponent's move
                score, _ = self.minimax(depth - 1, True, new_state)
                if score < best_score:
                    best_score = score
                    best_action = action

        return best_score, best_action
        

    # state = None for testing
    def _evaluate(self, state= None):
        
        board = state._table
        
        if state.isTerminated():
            # check winning 
            if state.get_winner_number() == 0:
                return 0
            elif state.get_winner_number() == 1:
                return -150
            elif state.get_winner_number() == 2:
                return 150
        
        diagonal_score = self._evaluate_2_and_3_in_row_diagonally(board)
        horizontal_score = self._evaluate_2_and_3_in_row_horizontally(board)
        vertical_score = self._evaluate_2_and_3_in_row_vertically(board)
        center_score = self._center_column_control(board)

        evaluation = diagonal_score + horizontal_score + vertical_score + center_score

        return evaluation
   
    def _evaluate_2_and_3_in_row_diagonally(self, board):
        

        result = [0,0]

        # Check diagonally (top-left to bottom-right)
        for d in range(-(self.cols-1), self.rows):
            count = 0
            prev_player = 0
            diagonal_positions = []  # Store [row, col] for each position in diagonal
            
            # Find all cells that belong to this diagonal
            for row in range(self.rows):
                col = row - d  
                if 0 <= col < self.cols:
                    diagonal_positions.append([row, col])
                    player = board[row][col]
                    
                    if player == 0:
                        count = 0
                        prev_player = 0
                    elif player == prev_player:
                        count += 1
                    else:
                        count = 1
                        prev_player = player 

                     # When we find 2 in a row
                    if count == 2 and prev_player != 0:
                        # Check open ends
                        has_left_open = False
                        has_right_open = False
                        
                        # Get positions of start and end of the sequence
                        start_row, start_col = diagonal_positions[-2]
                        end_row, end_col = diagonal_positions[-1]
                        
                        # Check left open end (one position before start)
                        if start_row - 1 >= 0 and start_col - 1 >= 0:
                            if board[start_row - 1][start_col - 1] == 0:
                                has_left_open = True
                        
                        # Check right open end (one position after end)
                        if end_row + 1 < self.rows and end_col + 1 < self.cols:
                            if board[end_row + 1][end_col + 1] == 0:
                                has_right_open = True
                        
                        # Score based on open ends
                        if has_left_open and has_right_open:
                            result[prev_player - 1] += 5  # Both ends open
                        elif has_left_open or has_right_open:
                            result[prev_player - 1] += 3  # One end open

                    # When we find 3 in a row
                    elif count == 3 and prev_player != 0:
                        # Check open ends
                        has_left_open = False
                        has_right_open = False
                        
                        # Get positions of start and end of the sequence
                        start_row, start_col = diagonal_positions[-3]
                        end_row, end_col = diagonal_positions[-1]
                        
                        # Check left open end (one position before start)
                        if start_row - 1 >= 0 and start_col - 1 >= 0:
                            if board[start_row - 1][start_col - 1] == 0:
                                has_left_open = True
                        
                        # Check right open end (one position after end)
                        if end_row + 1 < self.rows and end_col + 1 < self.cols:
                            if board[end_row + 1][end_col + 1] == 0:
                                has_right_open = True
                        
                        # Score based on open ends
                        if has_left_open and has_right_open:
                            result[prev_player - 1] += 15  # Both ends open
                        elif has_left_open or has_right_open:
                            result[prev_player - 1] += 12  # One end open
                        else:
                            result[prev_player - 1] += 8   # No open ends

        
        # check diagonaly (top-right to bottom-left)
        for d in range(self.rows + self.cols - 1): 
            count = 0
            prev_player = 0 
            diagonal_positions = []
            
            for row in range(self.rows):
                col = d - row 
                if 0 <= col < self.cols:
                    diagonal_positions.append([row, col])
                    player = board[row][col]

                    if player == 0:
                        count = 0
                        prev_player = 0
                    elif player == prev_player:
                        count += 1
                    else:
                        count = 1
                        prev_player = player 

                     # When we find 2 in a row
                if count == 2 and prev_player != 0:
                    # Check open ends
                    has_left_open = False
                    has_right_open = False
                    
                    # Get positions of start and end of the sequence
                    start_row, start_col = diagonal_positions[-2]
                    end_row, end_col = diagonal_positions[-1]
                    
                    # Check left open end (one position before start)
                    if start_row - 1 >= 0 and start_col + 1 < self.cols:
                        if board[start_row - 1][start_col + 1] == 0:
                            has_left_open = True
                    
                    # Check right open end (one position after end)
                    if end_row + 1 < self.rows and end_col - 1 >= 0:
                        if board[end_row + 1][end_col - 1] == 0:
                            has_right_open = True
                    
                    # Score based on open ends
                    if has_left_open and has_right_open:
                        result[prev_player - 1] += 5  # Both ends open
                    elif has_left_open or has_right_open:
                        result[prev_player - 1] += 3  # One end open

                    
                    elif count == 3 and prev_player != 0:
                        
                        has_left_open = False
                        has_right_open = False
                        
                        start_row, start_col = diagonal_positions[-3]
                        end_row, end_col = diagonal_positions[-1]
                        
                        if start_row - 1 >= 0 and start_col + 1 < self.cols:
                            if board[start_row - 1][start_col + 1] == 0:
                                has_left_open = True
                        
                        if end_row + 1 < self.rows and end_col - 1 >= 0:
                            if board[end_row + 1][end_col - 1] == 0:
                                has_right_open = True
                        
                        if has_left_open and has_right_open:
                            result[prev_player - 1] += 15 
                        elif has_left_open or has_right_open:
                            result[prev_player - 1] += 12 
                        else:
                            result[prev_player - 1] += 8  

        return result[0] - result[1]

    def _evaluate_2_and_3_in_row_horizontally(self, board):

        
        result = [0,0]

        for row in range(self.rows):
            prev_player = 0
            count = 0
            positions = []
            for col in range(self.cols):
                positions.append([row, col])
                player = board[row][col]

                if player == 0:
                    count = 0
                    prev_player = 0
                elif player == prev_player:
                    count += 1
                else:  # player != prev_player and player != 0
                    count = 1
                    prev_player = player

                # Check 2 in a row
                if count == 2 and prev_player != 0:
                    has_left_open = False
                    has_right_open = False

                    start_row, start_col = positions[-2]  # Fixed: Use -2 for two pieces
                    end_row, end_col = positions[-1]

                    # Check for left open
                    if start_col - 1 >= 0:
                        if board[start_row][start_col - 1] == 0:
                            has_left_open = True

                    # Check for right open
                    if end_col + 1 < self.cols:
                        if board[end_row][end_col + 1] == 0:
                            has_right_open = True

                    if has_left_open and has_right_open:
                        result[prev_player - 1] += 5  # Both ends open
                    elif has_left_open or has_right_open:
                        result[prev_player - 1] += 3  # One end open

                # Check 3 in a row
                elif count == 3 and prev_player != 0:
                    has_left_open = False
                    has_right_open = False

                    start_row, start_col = positions[-3]  # Correct for three pieces
                    end_row, end_col = positions[-1]

                    if start_col - 1 >= 0:
                        if board[start_row][start_col - 1] == 0:
                            has_left_open = True

                    if end_col + 1 < self.cols:
                        if board[end_row][end_col + 1] == 0:
                            has_right_open = True

                    if has_left_open and has_right_open:
                        result[prev_player - 1] += 15  # Both ends open
                    elif has_left_open or has_right_open:
                        result[prev_player - 1] += 12  # One end open
                    else:
                        result[prev_player - 1] += 8   # No open ends

        return result[0] - result[1] 
    
    def _evaluate_2_and_3_in_row_vertically(self, board):
        
        result = [0,0]

        # Check vertically
        for col in range(self.cols):
            prev_player = 0
            count = 0
            for row in range(self.rows):
                player = board[row][col]

                if player == 0:
                        count = 0
                        prev_player = 0
                elif player == prev_player:
                    count += 1
                elif player != prev_player:
                    count = 1
                    prev_player = player    
                
                # check 2 in a row
                if count == 2 and prev_player != 0 and row > 1 and board[row-2][col] == 0:
                    result[player-1] += 5  # One space above
                
                # check 3 in a row
                elif count == 3 and prev_player != 0:
                    if row > 2 and board[row-3][col] == 0:
                        result[player-1] += 15  # One space above
                    else:
                        result[player-1] += 8  # No space above

        return result[0] - result[1]

    def _center_column_control(self, board):
        center_col = self.cols // 2
        score = 0
    
        for row in range(self.rows):
            if board[row][center_col] == 1:
                score += 2
            elif board[row][center_col] == 2:
                score -= 2
        

        return score



# notes
# player 1 is maximizing
# player 2 is minimizing

# TODO
# Distance from Bottom
# Blocking Opponent's Threats:
# Fork Opportunities:
