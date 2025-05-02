from game_logic import State, ComputerPlayer
from tree import VisualTree, Node

debug = True
def log(msg):
    if debug:
        print(msg)



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
        # is_maximizing = (state.get_who_player_turn() == self.my_player_number)
        treeObject = VisualTree(-1, {'name': 'Root State'})
        _, action = self._minimax(treeObject, None, self.depth, True, state, alpha=float('-inf'), beta=float('inf'))
        treeObject.render_and_display()
        return action

    def _minimax(self, treeObject, parent_node_object, depth, is_maximizing, state, alpha=float("-inf"), beta=float("inf")):
        # return best_score, best_action
     
        parent_node_id = None if parent_node_object is None else parent_node_object.get_id()

        if depth == 0:
            value = self._evaluate(state)

            current_node_object = treeObject.add_node(parent_node_id, state.get_actions_list()[-1]+1, {"value": value, "remaning_depth":depth,"alpha":alpha, "beta": beta})

            return value, None 

        if state.is_terminate():
            value = self._evaluate(state)

            current_node_object = treeObject.add_node(parent_node_id, state.get_actions_list()[-1]+1, {"value": value, "winner_number": state.get_winner_player_number(), "remaning_depth":depth,"alpha":alpha, "beta": beta})

            return value, None 

        actions = state.get_available_actions()
        if not actions:
            value = self._evaluate(state)

            current_node_object = treeObject.add_node(parent_node_id, state.get_actions_list()[-1]+1, {"value": value, "remaning_depth":depth, "available_actions":[a+1 for a in actions],"alpha":alpha, "beta": beta})

            return value, None 
        

        best_action = None
        current_node_object = treeObject.add_node(parent_node_id, state.get_actions_list()[-1]+1, {"value": '?', "remaning_depth":depth, "available_actions":[a+1 for a in actions]})

        if is_maximizing:
            best_score = float('-inf')
            for action in actions:
                new_state = state.take_action_in_different_state_object(action)
                score, _ = self._minimax(treeObject, current_node_object, depth - 1, False, new_state, alpha, beta)

                
                if score > best_score or best_action is None:
                    best_score = score
                    best_action = action
                
                # alpha is the parent's max value
                # beta is the parent's min value


                if best_score > beta:
                # if score <= alpha:
                # if beta <= alpha:
                # if alpha <= beta:
                    print("beta <= alpha")
                    break

                # alpha = max(alpha, score)
                alpha = max(alpha, best_score)

        else:
            best_score = float('inf')
            for action in actions:
                new_state = state.take_action_in_different_state_object(action)
                score, _  = self._minimax(treeObject, current_node_object, depth - 1, True, new_state, alpha, beta)

                if score < best_score or best_action is None:
                    best_score = score
                    best_action = action
                
                if best_score < alpha:
                # if score >= beta:
                # if alpha <= beta:
                # if beta <= alpha:


                    print("alpha <= beta")
                    break


                #beta = min(beta, score)
                beta = min(beta, best_score)

        current_node_object.info["value"] = best_score
        current_node_object.info["player"] = "max" if is_maximizing else "min"
        current_node_object.info["best_next_action"] = best_action+1
        current_node_object.info["alpha"] = alpha
        current_node_object.info["beta"] = beta

        return best_score, best_action 

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
        center_col = self.cols // 2
        center_count = sum(1 for r in range(self.rows) if board[r][center_col] == self.my_player_number)
        score += center_count * 3

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
            score += 5
        elif count_self == 2 and count_empty == 2:
            score += 2

        if count_opp == 3 and count_empty == 1:
            score -= 4

        return score