# main code to run the program


def input_int(message, wrong_input_message, correct_values):
    while True:
        try:
            i = int(input(message))
        except:
            print(wrong_input_message)
        
        if i not in correct_values:
            print(wrong_input_message)
        else:
            return i


def command_line_program():
    pass #rich mode disaply

    from game_logic import Game, State, RandomPlayer,  HumanPlayerByCommandLine
    from game_ai import AiPlayer

    while True:
        print()
        print()
        print()
        print()
        print("--------------------------------")
        print("-------- Choose option ---------")
        print("--------------------------------")
        print()
        print(" 1. Player VS Player ")
        print(" 2. Player VS Ai ")
        print(" 3. exit ")
        print()
        print("--------------------------------")
        print()
        i = input_int("Choose option: ", "Please enter a valid option", (1,2,3))
        match i:
            case 1:
                g = Game([HumanPlayerByCommandLine("Player 1"), HumanPlayerByCommandLine("Player 2")])
                g.start_game()
            case 2:
                level = input_int("\n\n----- Choose the Ai level (1-5) -----\n 4 is recommended\n 5 is slow\nChoose: ", "Please enter a valid number", (i for i in range(1,5+1)))
                g = Game([HumanPlayerByCommandLine("You"), AiPlayer(name="Ai Player", level=level)])
                g.start_game()
            case 3:
                exit()
            case _: # default case
                print("Please enter a valid option")


def menu():
    while True:
        print()
        print("--------------------------------")
        print("-------- Choose progarm --------")
        print("--------------------------------")
        print()
        print(" 1. GUI program ")
        print(" 2. Command line program ")
        print(" 3. exit ")
        print()
        print("--------------------------------")
        print()
        i = input_int("Choose program: ", "Please enter a valid option", (1,2,3))
        match i:
            case 1:
                # Gui program
                from game_gui import start_gui
                start_gui()
                break
            case 2:
                command_line_program()
                break
            case 3:
                exit()
                break
            case _: # default case
                print("Please enter a valid option")

menu()
