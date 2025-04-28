from copy import deepcopy as copyOfObject
from abc import ABC, abstractmethod
from time import time
import random
import json

# For rich printing
import colorama
colorama.init(autoreset=True)


# Notes for editing ai code
# get_winner_number() is replaced by new is_terminate()
# take_action() and take_action_in_different_state_object() has no player number argument
# replaced is_game_of() with get_who_player_turn() and get_who_last_player_played_before_game_ended()
# replaced get_winner_number() with get_winner_player_number()
# replaced _get_winning_conditions() with get_winning_items_coordinates()
# changed get_player_action() arguments


class State():

    # Static constants
    ROWS_NUMBER=6
    COLUMNS_NUMBER=7
    WIN_NUMBER=4
    SYMBOLS = (0,1,2)
    

    def __init__(
        self,
        actions_list = None
    ):

        self._table = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
        self._actions_list = []


        # for get_termination_status() work
        self._last_termination_status = -1
        self._is_termination_status_checked = True
        self._last_action_coordinates = None 


        self._who_player_turn = 1 # first player
        self._winning_items_coordinates = None # None means (game not terminate) or (no one won)
        self._current_turn_number = 1

        # why can input actions_list ??
        # because of you want a state with particular board not init board

        if not actions_list is None:

            if not isinstance(actions_list,list):
                raise Exception("Not valid actions list")
            
            for i in range(len(actions_list)):
                try:
                    self.take_action(actions_list[i])
                except:
                    raise Exception(f"Not valid the action number '{i+1}' which is '{actions_list[i]}'")


    def display(self, withActionsRow=True, highlight_last_action=True, rich_display=True):
        "Prints the game board"

        if highlight_last_action:
            if self._current_turn_number == 1:
                last_y, last_x = (-1, -1)
            else:
                last_y, last_x = self.get_last_action_coordinates()

        if rich_display:
            print_style = ["", colorama.Fore.GREEN, colorama.Fore.RED]

        if withActionsRow:
            print("  (1  2  3  4  5  6  7)  ")
        for y in range(len(self._table)):
            print("[ ",end="")
            if rich_display:
                for x in range(len(self._table[y])):
                    if highlight_last_action and y == last_y and x == last_x:
                        print(print_style[self._table[y][x]]+"<●>",end="")
                    else:
                        print(print_style[self._table[y][x]]+" ● ",end="")
            else:
                for x in range(len(self._table[y])):
                    if highlight_last_action and y == last_y and x == last_x:
                        print("<"+str(self._table[y][x])+">",end="")
                    else:
                        print(" "+str(self._table[y][x])+" ",end="")
            print(" ]")


    def print_board_as_list(self):
        print(self._table)


    def get_board_as_list(self):
        return self._table


    def get_current_turn_number(self):
        """
        returns:
            if game ended: the turns was played
            if game not ended: the turn that should play it currently
        """
        return self._current_turn_number


    def get_actions_list(self):
        return self._actions_list


    def is_terminate(self):
        return self.get_termination_status() != -1


    def get_termination_status(self):
        """Checks if board is terminate
        & return termination status

        returns -1, 0, 1, 2
        -1 = not terminate
        0 = terminate and no one win
        1 = terminate and player 1 won
        2 = terminate and player 2 won
        """

        if not self._is_termination_status_checked:
            # not need to check if self._last_action_coordinates is None because if None implies that self._is_termination_status_checked = False

            y, x = self._last_action_coordinates
            symbol = self._table[y][x] # last player played number

            # check win Vertically
            if y < 3 and self._table[y+1][x] == symbol and self._table[y+2][x] == symbol and self._table[y+3][x] == symbol:
                self._last_termination_status = symbol

            # check win Horizontally
            if self._last_termination_status == -1:
                count = 1
                for i in range( max(0, x-1) ,  max(0, x-3) -1 , -1 ):
                    if self._table[y][i] == symbol:
                        count += 1
                    else:
                        break
                for i in range( max(0, x+1) , min(6, x+3) +1 ):
                    if self._table[y][i] == symbol:
                        count += 1
                    else:
                        break
                if count > 3:
                    self._last_termination_status = symbol

            # check win Diagonally ( \ )
            if self._last_termination_status == -1:
                count = 1
                for i in range( 1, 4 ):
                    if y-i > -1 and x-i > -1 and self._table[y-i][x-i] == symbol:
                        count += 1
                    else:
                        break
                for i in range( 1, 4 ):
                    if y+i < 6 and x+i < 7 and self._table[y+i][x+i] == symbol:
                        count += 1
                    else:
                        break
                if count > 3:
                    self._last_termination_status = symbol

            # check win Diagonally ( / )
            if self._last_termination_status == -1:
                count = 1
                for i in range( 1, 4 ):
                    if y-i > -1 and x+i < 7 and self._table[y-i][x+i] == symbol:
                        count += 1
                    else:
                        break
                for i in range( 1, 4 ):
                    if y+i < 6 and x-i > -1 and self._table[y+i][x-i] == symbol:
                        count += 1
                    else:
                        break
                if count > 3:
                    self._last_termination_status = symbol


            # Check if board is full
            if self._last_termination_status == -1:
                if all([item != 0 for item in self._table[0]]):
                    self._last_termination_status = 0
            
            self._is_termination_status_checked = True

        return self._last_termination_status
    

    def take_action(self, action):
        
        # Check if gamed ended
        if self.get_termination_status() != -1:
            raise Exception("Game ended, No available action.")

        # Check that it is an available action
        if not self.is_available_action(action):
            raise Exception("Not available action")
        
        # make action
        player_number = self.get_who_player_turn()
        found = False
        for y in range(1, self.ROWS_NUMBER):
            # the first row must be checked by self.is_available_action() so start range from 1 not 0
            if self._table[y][action] != 0:
                # Once find frist un empty place, put in before it (top of it)
                self._table[y-1][action] = player_number
                self._last_action_coordinates = (y-1, action)
                found = True
                break
        # if checked all rows and all are empty, put in the lower row
        if not found:
            self._table[ self.ROWS_NUMBER - 1 ][action] = player_number
            self._last_action_coordinates = (self.ROWS_NUMBER - 1, action)        

        # Record action
        self._actions_list.append(action)

        # now, termination status isn't checked, need recheck
        self._is_termination_status_checked = False

        # recheck termination status
        termination_status = self.get_termination_status()

        if termination_status == -1:
            # toggle player
            self._toggle_player_turn()

            # increase the turn number
            self._current_turn_number += 1


    def take_action_in_different_state_object(self, action):
        new_state = copyOfObject(self)
        new_state.take_action(action)
        return new_state


    def is_available_action(self, action):
        return 0 <= action < self.COLUMNS_NUMBER and self._table[0][action] == 0
    

    def get_available_actions(self):
        return [ action for action in range(0, self.COLUMNS_NUMBER) if self._table[0][action] == 0 ]
    

    def get_last_action_coordinates(self):
        """
        returns: 
            if no player played yet: error
            if a player played: tuple like (y, x) of size two
                y is the row index, start from top to bottom 0, 1, 2, ...
                x is the column index, start from left to right 0, 1, 2, ...
        """

        if self._last_action_coordinates is None:
            raise Exception("No player played yet.")

        return self._last_action_coordinates


    def get_winning_items_coordinates(self):
        """returns coordinates of win items on board
        return coordinates in format as in get_last_action_coordinates() explaination
        
        returns:
            error if Game is not ended
            error if Game is ended and there is no winner
            list of coordinates if Game is ended and there is a winner
        """
        
        termination_status = self.get_termination_status()
        
        if termination_status == -1:
            raise Exception("Game is not ended")
        
        if termination_status == 0:
            raise Exception("No one won.")

        return self._calc_winning_items_coordinates()

    def _calc_winning_items_coordinates(self):
        "Helper function for get_winning_items_coordinates()"
        pass

    def get_who_player_turn(self):
        """
        Only works if game not ended

        returns:
            1 if player 1
            2 if player 2
            error if game ended
        """

        if self.get_termination_status() != -1:
            raise Exception("Game Ended")

        return self._who_player_turn


    def get_who_last_player_played_before_game_ended(self):
        """
        Only works if game ended

        returns:
            1 if player 1
            2 if player 2
            error if game is not ended
        """

        if self.get_termination_status() == -1:
            raise Exception("Game is not ended")

        return self._who_player_turn


    def get_winner_player_number(self):
        """
        Only works if game ended

        returns:
            0 if no one won
            1 if player 1
            2 if player 2
            error if game is not ended
        """

        # Note about usage:
        # generally you do not need this function if you use get_termination_status()
        # but need it if you use is_terminate()

        # Note about code: 
        # winner player not always the last player played, may no one won

        termination_status = self.get_termination_status()

        if termination_status == -1:
            raise Exception("Game is not ended")
        
        return termination_status
    

    def _toggle_player_turn(self):
        if self.get_termination_status() != -1:
            raise Exception("Game Ended")

        # toggle between 1 and 2
        self._who_player_turn = 3 - self._who_player_turn
        
# -----------------------------------------------------------

class Player(ABC):
    def __init__(self, name = "Player"):
        self.name = name

    @abstractmethod
    def get_player_action(self, copy_of_current_state):
        """This function is called by Game class and returns the action that the user choosed
            returns: player_action"""
        pass
    
    @abstractmethod
    def get_default_name(self):
        "Help know what is type of player"

        return "Player"

class ComputerPlayer(Player, ABC):
    "Refers to Ai player or computer player"

    def get_player_action(self, copy_of_current_state):
        pass

    def get_default_name(self):
        return "Ai Player"

class RandomPlayer(ComputerPlayer):
    "player play random action, takes 1 milisecond or less to take action"

    def __init__(self, name = "Player"):
        super().__init__(name)
        self.rng = random.Random() 

    def get_player_action(self, copy_of_current_state):
        return self.rng.choice(copy_of_current_state.get_available_actions())


    def get_default_name(self):
        return "Ai Player"



class HumanPlayer(Player, ABC):
    @abstractmethod
    def get_player_action(self, copy_of_current_state):
        pass

    def get_default_name(self):
        return "Human Player"


class HumanPlayerByGUI(HumanPlayer):
    def get_player_action(self, copy_of_current_state):
        pass

class HumanPlayerByCommandLine(HumanPlayer):
    def get_player_action(self, copy_of_current_state: State):
        copy_of_current_state.display(True, True)
        available_actions = copy_of_current_state.get_available_actions()
        while True:
            try:
                action = int(input(f"{self.name}, Choose action: "))-1
                if action in available_actions:
                    
                    print("-"*50)
                    return action
                else:
                    print("Wrong action")
            except:
                print("Wrong action")

# -----------------------------------------------------------

class Game():
    def __init__(self, players, init_state = None, output_file = "games_history.json"):
        if not (isinstance(players, (list,tuple)) and len(players) == 2 and all([isinstance(p, Player) for p in players])):
            raise Exception("Enter correct players")
        self._players = players
        if init_state is None:
            self._current_state = State()
        else:
            self._current_state = init_state
        self._init_state = copyOfObject(self._current_state)
        self.actions_history = []
        self.times_history = []
        self.output_file = output_file

    def start_game(self):
        
        if self.is_game_over():
            self.game_over()
            return

        player_turn = self._current_state.get_who_player_turn() - 1

        while not self.is_game_over():


            time_of_player = time()
            
            # get player action
            action = self._players[player_turn].get_player_action(copyOfObject(self._current_state))

            time_of_player = time() - time_of_player

            if not self._current_state.is_available_action(action):
                raise Exception("Player sended to Game Object a wrong action")
            
            self.actions_history.append(action)
            self.times_history.append(time_of_player)
            self._current_state.take_action(action)
            player_turn = 1 - player_turn

            print(f"{self._players[player_turn].name} took {time_of_player:.2f}sec to play")

        self.game_over()



    def game_over(self):
        "Called when game ended"

        print("-"*50)
        print("")
        self._current_state.display()

        winner = self._current_state.get_winner_player_number()
        if winner in (1,2):
            print(f"Player {winner} is The Winner. ({self._players[winner-1].name})")
        elif winner == 0:
            print(f"No one won.")
        else:
            raise Exception("unexpected error")

        # record result
        with open(self.output_file, "a") as file:
            file.write(",\n") 
            file.write(json.dumps(
                {
                    "players": [player.name for player in self._players],
                    "init_state_actions_list": self._init_state.get_actions_list(),
                    "actions": self.actions_history,
                    "times": self.times_history,
                    "winner": winner if winner in [0, 1, 2] else "error"
                }, 
                indent=4
            )) 
            


    def is_game_over(self):
        return self._current_state.is_terminate()


