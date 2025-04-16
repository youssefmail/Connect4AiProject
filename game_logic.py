from copy import deepcopy as copyOfObject
from abc import ABC, abstractmethod
from time import time
import random

# INIT_STATE_TABLE = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]
def GET_INIT_STATE():
    return State([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])

DEBUG_MODE = True
def log(message):
    if DEBUG_MODE:
        if isinstance(message,(str,int,float)):
            print("Log: "+str(message))
        else:
            print(message)


def intersection(list1, list2):
    "get intersection of items in two lists"

    if len(list1) < len(list2):
        return [item for item in list1 if item in list2]
    else:
        return [item for item in list2 if item in list1]

    # another way failed with me
    # Important note: return them without consider the order
    # return list(set(list1) & set(list2))
    # # Code in more clear way
    # set1 = set(list1)
    # set2 = set(list2)
    # intersection_set = set1 & set2
    # intersection_list = list(intersection_set)

# class Action():
#     def __init__(self,x,y,value):
#         self.x = x
#         self.y = y
#         self.value = value

class State():
    def __init__(
        self,
        table,
        action = None,
        SYMBOLS = [0,1,2],
        ROWS_NUMBER=6,
        COLUMNS_NUMBER=7,
        WIN_NUMBER=4,
    ):
        if not isinstance(table,list):
            raise Exception("Not Table")
        
        self._table = table
    
        self.ROWS_NUMBER = ROWS_NUMBER
        self.COLUMNS_NUMBER = COLUMNS_NUMBER
        self.WIN_NUMBER = WIN_NUMBER
        self.SYMBOLS = SYMBOLS
    
        if not self.isCorrectTable():
            raise Exception("Not Correct Table")
        
        self._isTerminatedBoolean = None

    def isCorrectTable(self):
        "Checks if table is a correct connect 4 game"

        # Check data type
        if not isinstance(self._table,list): return False
        for row in self._table:
            if not isinstance(row,list): return False
        for row in self._table:
            for item in row:
                if not isinstance(item,(int,str)):
                    return False
            
        # Check Dimensions and lengths
        if len(self._table) != self.ROWS_NUMBER: return False
        for row in self._table:
            if len(row) != self.COLUMNS_NUMBER: return False

        # Check allowed symbols (0,1,2)
        # count2 أو count1 == count2 + 1
        # dic = {}
        # for x in range(0,self.COLUMNS_NUMBER):
        #     for y in range(0,self.ROWS_NUMBER):
        #         dic[self._table[y][x]] += 1
        # TODO

        # Check logic (items in table are logical)
        for x in range(0,self.COLUMNS_NUMBER):
            found_frist_non_empty = False
            for y in range(0,self.ROWS_NUMBER):
                if self._table[y][x] != self.SYMBOLS[0]:
                    found_frist_non_empty = True
                else:
                    if found_frist_non_empty:
                        return False

        


        # check winning conditions
        if not self._is_correct_winning_conditions():
            return False


        return True

    def _is_correct_winning_conditions(self):
        """Helper function for isCorrectTable()"""
        # check winning conditions (Not both win, Not win multiple times for same player) if exist
        
        winning_conditions = self._get_winning_conditions()

        if not winning_conditions:
            return True
        else:

            # Must there is an item in "S" that if deleted will not find any winning conditions
            # else: the state is not correct
            S = intersection(winning_conditions, self._get_upper_items_coordinates())
            del winning_conditions # not need it

            if not S: # if empty list
                return False

            for item in S:
                new_state = copyOfObject(self)
                new_state._table[item[0]][item[1]] = self.SYMBOLS[0]
                if not new_state._get_winning_conditions(): # if empty list
                    return True

            return False


    def _get_winning_conditions(self):
        """Helper function for _is_correct_winning_conditions()"""

        winning_conditions = []

        # Horizontally
        for y in range(0, self.ROWS_NUMBER):
            last_item_seen = self._table[y][0]
            counter = 1
            for x in range(1, self.COLUMNS_NUMBER):
                if self._table[y][x] == last_item_seen:
                    counter += 1
                    if counter == self.WIN_NUMBER and last_item_seen != self.SYMBOLS[0]:
                        for i in range(0, self.WIN_NUMBER):
                            winning_conditions.append([ y , x - self.WIN_NUMBER + 1 + i ])
                        # winning_conditions.append([
                        #     y,
                        #     x - self.WIN_NUMBER + 1,
                        #     "to right"
                        # ])
                        counter = 0
                else:
                    last_item_seen = self._table[y][x]
                    counter = 1

        
        # Vertically
        for x in range(0, self.COLUMNS_NUMBER):
            last_item_seen = self._table[0][x]
            counter = 1
            for y in range(1, self.ROWS_NUMBER):
                if self._table[y][x] == last_item_seen:
                    counter += 1
                    if counter == self.WIN_NUMBER and last_item_seen != self.SYMBOLS[0]:
                        for i in range(0, self.WIN_NUMBER):
                            winning_conditions.append([ y - self.WIN_NUMBER + 1 + i , x ])
                        # winning_conditions.append([
                        #     y - self.WIN_NUMBER + 1,
                        #     x,
                        #     "to down"
                        # ])
                        counter = 0
                else:
                    last_item_seen = self._table[y][x]
                    counter = 1


        # Diagonally, Form up left to down right
        for y in range(0, self.ROWS_NUMBER - self.WIN_NUMBER + 1):
            for x in range(0, self.COLUMNS_NUMBER - self.WIN_NUMBER + 1):
                main_item = self._table[y][x]
                if main_item != self.SYMBOLS[0]:
                    if all( [self._table[y+i][x+i] == main_item for i in range(0, self.WIN_NUMBER)]):
                        for i in range(0, self.WIN_NUMBER):
                            winning_conditions.append([ y+i , x+i ])
                        
                        # winning_conditions.append([
                        #     y,
                        #     x,
                        #     "to right down"
                        # ])


        # Diagonally, Form up right to down left
        for y in range(0, self.ROWS_NUMBER - self.WIN_NUMBER + 1):
            for x in range(self.WIN_NUMBER - 1, self.COLUMNS_NUMBER):
                main_item = self._table[y][x]
                if main_item != self.SYMBOLS[0]:
                    if all([self._table[y+i][x-i] == main_item for i in range(0, self.WIN_NUMBER)]):
                        for i in range(0, self.WIN_NUMBER):
                            winning_conditions.append([ y+i , x-i ])


                        # winning_conditions.append([
                        #     y,
                        #     x,
                        #     "to left down"
                        # ])

        
        return winning_conditions


    def _get_upper_items_coordinates(self):
        "returns list of coordinates of items that is in the top of each column"

        lst = []
        for x in range(0,self.COLUMNS_NUMBER):
            for y in range(0,self.ROWS_NUMBER):
                if self._table[y][x] != self.SYMBOLS[0]:
                    lst.append([y,x])
                    break
        
        return lst

    def _check_count_of_items(self):
        count_of_items = self._get_count_of_items()

        for key in count_of_items:
            if not key in self.SYMBOLS:
                return False

        return items_count[self.SYMBOLS[1]] == items_count[self.SYMBOLS[2]] or items_count[self.SYMBOLS[1]] == items_count[self.SYMBOLS[2]] + 1
    
    def _get_count_of_items(self):
        items_count = {symbol: 0 for symbol in self.SYMBOLS}

        for row in self._table:
            for item in row:
                items_count[item] += 1

        return items_count

    def display(self, withActionsRow):
        "Prints the game table"
        if withActionsRow:
            print("  (1  2  3  4  5  6  7)  ")
        for row in self._table:
            print("[  ",end="")
            for item in row:
                print(str(item)+"  ",end="")
            print("] ")

    def printAsList(self):
        print(self._table)

    def getAsList(self):
        return self._table


    def isTerminated(self):
        "Checks if the state is end of game or not"

        if self._isTerminatedBoolean is None or self._isTerminatedBoolean == False:
            if all([item != self.SYMBOLS[0] for item in self._table[0]]):
                self._isTerminatedBoolean = True

        if self._get_winning_conditions():
            self._isTerminatedBoolean = True

        return self._isTerminatedBoolean

    def get_winner_number(self):
        "returns: 0, 1, 2 or error"

        if not self.isTerminated():
            raise Exception("Not terminated to know the winner")
        
        lst = self._get_winning_conditions()

        if not lst:
            return 0
        
        return self._table[lst[0][0]][lst[0][1]]
    
    def take_action(self, action, player_number):
        if not self.is_available_action(action):
            raise Exception("Not available action")
        
        lst = []
        for y in range(0, self.ROWS_NUMBER):
            if self._table[y][action] != self.SYMBOLS[0]:
                self._table[y-1][action] = self.SYMBOLS[player_number]
                return
        self._table[ self.ROWS_NUMBER - 1 ][action] = self.SYMBOLS[player_number]

    def take_action_in_different_state_object(self, action, player_number):
        new_state = copyOfObject(self)
        new_state.take_action(action, self.SYMBOLS[player_number])
        return new_state

    def is_available_action(self, action):
        return 0 <= action < self.COLUMNS_NUMBER and self._table[0][action] == self.SYMBOLS[0]
    
    def get_available_actions(self):
        return [ action for action in range(0, self.COLUMNS_NUMBER) if self._table[0][action] == self.SYMBOLS[0] ]
        
    def is_game_of(self):
        "returns 0, 1 or 2 which is the player who is his turn"
        
        count_of_items = self._get_count_of_items()

        if count_of_items[self.SYMBOLS[1]] == count_of_items[self.SYMBOLS[2]]:
            return 1
        elif count_of_items[self.SYMBOLS[1]] == count_of_items[self.SYMBOLS[2]] + 1:
            return 2
        else:
            return 0




# GET_INIT_STATE().isTerminated()
# x = State([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,1,1,1,1,0]])
# x = State([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,2],[0,0,0,0,0,0,2],[0,0,0,0,0,0,2],[0,0,1,1,1,1,2]])
# x = State([[3,0,0,0,0,0,0],[3,0,0,0,0,0,0],[3,0,0,0,0,0,0],[3,0,0,0,0,0,0],[2,0,0,0,0,0,0],[1,0,1,1,1,1,0]])
# x = State([[3,1,2,3,8,8,8],[3,4,5,6,8,8,8],[3,7,9,10,8,8,8],[3,11,12,13,8,8,8],[2,8,8,8,8,8,8],[1,8,1,1,1,1,8]])
# # x.display()
# # x = State([[0,0,2,0,8,0,2],[3,4,5,6,8,2,8],[3,7,9,10,2,8,8],[3,11,12,2,8,8,8],[2,8,8,8,8,8,8],[1,8,1,1,1,1,8]])
# # x.display()

class Player(ABC):
    def __init__(self, name = "Player"):
        self.name = name

    @abstractmethod
    def get_player_action(self, copy_of_current_state):
        "This function is called by Game class and returns the action that the user choosed"
        pass

    def get_default_name(self):
        return "Player"

class AiPlayer(Player):
    def get_player_action(self, copy_of_current_state):
        pass

    def get_default_name(self):
        return "Ai Player"

class RandomPlayer(AiPlayer):
    def get_player_action(self, copy_of_current_state):
        return random.choice(copy_of_current_state.get_available_actions())

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
        print("-"*50)
        copy_of_current_state.display(True)
        available_actions = copy_of_current_state.get_available_actions()
        while True:
            try:
                action = int(input(f"{self.name}, Choose action: "))-1
                if action in available_actions:
                    return action
                else:
                    print("Wrong action")
            except:
                print("Wrong action")

class Game():
    def __init__(self, players, init_state = GET_INIT_STATE(), name = time()):
        if not (isinstance(players, list) and len(players) == 2):
            raise Exception("Enter correct players")
        self._players = players
        self._current_state = init_state
        self._init_state = copyOfObject(self._current_state)
        self.actions_history = []
        self._is_game_over_boolean = None
        self.is_game_over()
        self.name = name

    def start_game(self):
        
        if self.is_game_over():
            self.game_over()
            return

        player_turn = self._current_state.is_game_of()

        if not player_turn in [1,2]:
            raise Exception("Unexpected error")

        player_turn -= 1

        while not self.is_game_over():
            action = self._players[player_turn].get_player_action(copyOfObject(self._current_state))
            if not action in self._current_state.get_available_actions():
                raise Exception("Player sended to Game Object a wrong action")
            self.actions_history.append(action)
            self._current_state.take_action(action, player_turn+1)

            player_turn = 1 - player_turn # toggle players

        self.game_over()



    def game_over(self):
        "Called when game ended"

        winner = self._current_state.get_winner_number()
        if winner in [1,2]:
            print(f"Player {winner} is The Winner. ({self._players[winner-1].name})")
        elif winner == 0:
            print(f"No one is the Winner")
        else:
            raise Exception("unexpected error")

        # write result
        with open(f"games.csv", "a") as file:
            file.write("\n{")
            file.write("\n\"players\": "+str([player.name for player in self._players])+",")
            file.write("\n\"init_state\": "+str(self._init_state.getAsList())+",")
            file.write("\n\"actions\": "+str(self.actions_history))
            file.write("\n\"winner\": "+(str(winner) if winner in [0, 1, 2] else "error")+",")
            file.write("\n},")
            file.write("\n")

    def is_game_over(self):
        if self._is_game_over_boolean is None or self._is_game_over_boolean == False:
            self._is_game_over_boolean = self._current_state.isTerminated()
        return self._is_game_over_boolean


