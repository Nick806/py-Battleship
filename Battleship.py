"""

Significato dei simboli nelle tabelle:

    Tabella di attacco (caratteri):
        "O" = non noto / non ancora sparato
        "A" = Acqua
        "X" = Colpito ma non affondato
        "Y" = Colpito e affondato

    Tabella di difesa (int):
        0 = vuoto
        1 = nave da 2
        2 = nave da 2
        3 = nave da 2
        4 = nave da 3
        5 = nave da 3
        6 = nave da 4
        7 = nave da 4
        8 = nave da 5


"""


import random
import time
import os
import importlib
import configparser

random_bot_ship_placer = "Bots\RandomBot.py"

################################################################################
#   Settings functions
################################################################################

class symbols:
    def __init__(self, unknown, miss, hit, sunk):
        self.unknown = unknown
        self.miss = miss
        self.hit = hit
        self.sunk = sunk

#set the default value of every variable
default_symbols = symbols("O", "A", "X", "Y")
config_symbols = symbols("O", "A", "X", "Y")

ROWS = 10
COLUMNS = 10
SHIPS = [2,2,2,2,3,3,3,4,4,5]

bots_folder = "Bots"

def retrive_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    config_symbols.unknown = str(config.get('symbols', 'unknown'))
    config_symbols.miss = str(config.get('symbols', 'miss'))
    config_symbols.hit = str(config.get('symbols', 'hit'))
    config_symbols.sunk = str(config.get('symbols', 'sunk'))

    SHIPS = list(map(int, config.get('game', 'ships').split(',')))
    ROWS = int(config.get('game', 'rows'))
    COLUMNS = int(config.get('game', 'columns'))

    bots_folder = config.get('settings', 'bots_folder')


################################################################################
#   GUI functions
################################################################################

def print_start():
    name = """
                            $$$$$$$\             $$\     $$\     $$\                     $$\       $$\           
                            $$  __$$\            $$ |    $$ |    $$ |                    $$ |      \__|          
 $$$$$$\  $$\   $$\         $$ |  $$ | $$$$$$\ $$$$$$\ $$$$$$\   $$ | $$$$$$\   $$$$$$$\ $$$$$$$\  $$\  $$$$$$\  
$$  __$$\ $$ |  $$ |$$$$$$\ $$$$$$$\ | \____$$\\\_$$  _|\_$$  _|  $$ |$$  __$$\ $$  _____|$$  __$$\ $$ |$$  __$$\ 
$$ /  $$ |$$ |  $$ |\______|$$  __$$\  $$$$$$$ | $$ |    $$ |    $$ |$$$$$$$$ |\$$$$$$\  $$ |  $$ |$$ |$$ /  $$ |
$$ |  $$ |$$ |  $$ |        $$ |  $$ |$$  __$$ | $$ |$$\ $$ |$$\ $$ |$$   ____| \____$$\ $$ |  $$ |$$ |$$ |  $$ |
$$$$$$$  |\$$$$$$$ |        $$$$$$$  |\$$$$$$$ | \$$$$/  \$$$$  |$$ |\$$$$$$$\ $$$$$$$  |$$ |  $$ |$$ |$$$$$$$  |
$$  ____/  \____$$ |        \_______/  \_______|  \____/  \____/ \__| \_______|\_______/ \__|  \__|\__|$$  ____/ 
$$ |      $$\   $$ |                                                                                   $$ |      
$$ |      \$$$$$$  |                                                                                   $$ |      
\__|       \______/                                                                                    \__|      

beta version                                                                                        by Nick806
"""
    print(name)

def input_gamemode():
    modes = """

Select a game mode [1-3]:

1) Uman gamepay whit random bot ship positioning
2) Step-by-step Bot gameplay whit random bot ship positioning (you can choose the bot that will play)
3) Automatic and loop Bot gamepay whit random bot ship positioning (you can choose the bot that will play)

Gamemode n°... """
    return input(modes)

def play_gamemode(gamemode):

    gamemode = int(gamemode)

    if gamemode == 1:
        gamemode1()

    elif gamemode == 2:
        gamemode2()

    elif gamemode == 3:
       print("Still to do (3)")

################################################################################
#   Section with basic functions
################################################################################

def create_table(rows, columns, elements):
    """
    Creates a 2D table (list of lists) with the specified number of rows and columns,
    filling each cell with the provided elements.

    Parameters:
    - rows (int): The number of rows in the table.
    - columns (int): The number of columns in the table.
    - elements: The value to be placed in each cell of the table.

    Returns:
    - list: A 2D table represented as a list of lists.
    """
    table = [[elements for _ in range(columns)] for _ in range(rows)]
    return table

def print_table(table):
    """
    Prints the elements of a 2D table in a readable format.

    Parameters:
    - table (list): A 2D table represented as a list of lists.

    Prints:
    - Displays the elements of the table, with each row on a new line.
    """
    for row in table:
        for item in row:
            print(item, end=" ")
        print()

def print_attack(table):
    """
    Prints the elements of an attack table in a readable format.

    Parameters:
    - table (list): A 2D table represented as a list of lists.

    Prints:
    - Displays the elements of the attac table, with the selected icons.
    """
    for row in table:
        for item in row:
            if item == default_symbols.hit:
                print(config_symbols.hit, end=" ")
            elif item == default_symbols.miss:
                print(config_symbols.miss, end=" ")
            elif item == default_symbols.sunk:
                print(config_symbols.sunk, end=" ")
            elif item == default_symbols.unknown:
                print(config_symbols.unknown, end=" ")
        print()

def count_element_in_table(table, element):
    """
    Returns the number of times an element is contained in a table.

    Parameters:
    - table (list): The table in which to count occurrences of the element.
    - element: The element to count.

    Returns:
    - int: The count of occurrences of the specified element in the table.
    """
    count = 0

    for row in table:
        count += row.count(element)

    return count

def attack(attack_table, ship_positioning_table, row, columns):
    """
    Performs an attack on a specified position in the target ship_positioning_table.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.
    - ship_positioning_table (list): The table representing the positions of ships, where 0 denotes an empty position.
    - row (int): The row of the attack position (index of the array = row - 1).
    - column (int): The column of the attack position (index of the array = column - 1).

    Modifies:
    - Modifies the attack_table based on the outcome of the attack.
    """
    row -= 1
    columns -= 1
    if attack_table[row][columns] == "O":
        if ship_positioning_table[row][columns] == 0:
            attack_table[row][columns] = "A"
        else:
            attack_table[row][columns] = "X"

def check_hit_and_sunk(attack_table, ship_positioning_table, row, columns):
    """
    Checks if an attack hit and sunk a ship at the specified position.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.
    - ship_positioning_table (list): The table representing the positions of ships, where 0 denotes an empty position.
    - row (int): The row index of the attack position (1-indexed).
    - columns (int): The column index of the attack position (1-indexed).

    Note:
    - If the attack did not hit a ship or the ship is not completely sunk, the function returns without any action.
    - If the attack hit and sunk a ship, the function marks all parts of the ship with "Y" in the attack_table.
    """
    row -= 1
    columns -= 1

    ship_number = ship_positioning_table[row][columns]

    if ship_number == 0:
        return  # No ship is hit

    # Check if there are remaining pieces of the ship
    for r in range(len(ship_positioning_table)):
        for c in range(len(ship_positioning_table[0])):
            if ship_positioning_table[r][c] == ship_number and attack_table[r][c] == "O":
                return  # Ship is not completely sunk, exit function

    # If all pieces of the ship are hit, mark them as sunk
    for r in range(len(ship_positioning_table)):
        for c in range(len(ship_positioning_table[0])):
            if ship_positioning_table[r][c] == ship_number:
                attack_table[r][c] = "Y"

def check_win(attack_table, ship_positioning_table):
    """
    Checks if the player has won the game by successfully sinking all the ships.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.
    - ship_positioning_table (list): The table representing the positions of ships, where 0 denotes an empty position.

    Returns:
    - int: 1 if the player has won (all ships are sunk), 0 otherwise.
    """
    # Contains all the remaining parts to be hit
    remaining_pieces = create_table(len(attack_table), len(attack_table[0]), 0)

    # Compare the two tables
    for row in range(len(remaining_pieces)):
        for col in range(len(remaining_pieces[0])):
            if attack_table[row][col] == "O":
                remaining_pieces[row][col] = ship_positioning_table[row][col]

    # Check for any remaining ship parts
    for row in range(len(remaining_pieces)):
        for col in range(len(remaining_pieces[0])):
            if remaining_pieces[row][col] != 0:
                return 0  # Player has not yet won

    return 1  # Player has won

def get_remaining_ships(attack_table, ship_positioning_table, ships):
    """
    Retrieves the list of remaining ships based on the current state of the game.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.
    - ship_positioning_table (list): The table representing the positions of ships, where 0 denotes an empty position.
    - ships (list): The list of all ships in the game.

    Returns:
    - list: A list containing the names of the remaining ships based on the current state of the game.
    """
    # Contains all the remaining parts to be hit
    remaining_pieces = create_table(len(attack_table), len(attack_table[0]), 0)

    # Compare the two tables
    for row in range(len(remaining_pieces)):
        for col in range(len(remaining_pieces[0])):
            if attack_table[row][col] == "O":
                remaining_pieces[row][col] = ship_positioning_table[row][col]

    remaining_ships = []
    for ship_index in range(len(ships)):
        if count_element_in_table(remaining_pieces, ship_index + 1) > 0:
            remaining_ships.append(ships[ship_index])

    return remaining_ships

def get_ships(table):
    """
    Retrieves the number of ships in the table.

    Parameters:
    - table (list): The table representing the positions of ships, where 0 denotes an empty position.

    Returns:
    - list: A list containing the number of ships in the table.
    """
    number_of_ships = max(max(table, key=max))
    ship_counts = []

    for num in range(number_of_ships):
        ship_counts.append(count_element_in_table(table, num + 1))

    return ship_counts


################################################################################
#   Section with different game modes
################################################################################

def gamemode1():
    ship_positioning_table = create_table(ROWS, COLUMNS, 0)
    execute_function(random_bot_ship_placer, "place_ships", ship_positioning_table, SHIPS)
    game(create_table(ROWS, COLUMNS, "O"), ship_positioning_table)


def game(attack_table, ship_positioning_table):
    """
    Initiates and manages the gameplay loop.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.
    - ship_positioning_table (list): The table representing the positions of ships, where 0 denotes an empty position.

    Note:
    - The function manages the player's turns, taking input for row and column to perform an attack.
    - It then updates the attack table and checks for hits and sunk ships.
    - The game continues until the player wins.
    """
    moove = 0

    ships = SHIPS
    while True:
        print_attack(attack_table)
        
        moove += 1
        print("Moove number " + str(moove))
        remaining_ships = get_remaining_ships(attack_table, ship_positioning_table, ships)
        print("Remaining ships: " + str(remaining_ships))

        while True:
            try:
                row = int(input("Row: "))
                column = int(input("Column: "))
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue  # Go back to the start of the loop if the input is not valid

            break  # Exit the loop if the input is valid

        attack(attack_table, ship_positioning_table, row, column)
        check_hit_and_sunk(attack_table, ship_positioning_table, row, column)
        
        if check_win(attack_table, ship_positioning_table):
            print_attack(attack_table)
            print("You won!")
            return


def gamemode2():
    ship_positioning_table = create_table(ROWS, COLUMNS, 0)
    execute_function(random_bot_ship_placer, "place_ships", ship_positioning_table, SHIPS)
    ships = SHIPS

    bot_directory =os.path.join(bots_folder, input("Name of the bot (with file extension): "))

    attack_table = create_table(ROWS, COLUMNS, "O")

    moove = 0
    while True:
        print_attack(attack_table)
        
        moove += 1
        print("Moove number " + str(moove))

        remaining_ships = get_remaining_ships(attack_table, ship_positioning_table, ships)
        print("Remaining ships: " + str(remaining_ships))

        row, column = execute_function(bot_directory, "take_shot", attack_table, remaining_ships)

        print ("Row: " + str(row) + "   Column: " + str(column))

        input("Press ENTER to step")

        print(" ")


        attack(attack_table, ship_positioning_table, row, column)
        check_hit_and_sunk(attack_table, ship_positioning_table, row, column)
        
        if check_win(attack_table, ship_positioning_table):
            print_attack(attack_table)
            print("You won! (" + str(moove) + " mooves)")
            return


#TODO Write this in english
        
def gioco_bot(tabella_attacco, tabella_difesa, navi, bot_directory):

    conta_mosse = 0

    while True:
        conta_mosse += 1

        """print_table(tabella_attacco)
        print("")
        print("Mossa numero " + str(conta_mosse))
        print("")
        #print_table(legal_moves_table(tabella_attacco))
        #print("")
        #print(legal_moves_list(tabella_attacco))
        #print("")
        #print(len(legal_moves_list(tabella_attacco)))
        #print("")
        #print(get_remaining_ships(tabella_attacco, tabella_difesa, navi))
        #print("")
        print_table(calculate_probability_table(tabella_attacco, get_remaining_ships(tabella_attacco, tabella_difesa, navi)))
        print("")"""


        riga, colonna = execute_function(bot_directory, "take_shot", tabella_attacco, get_remaining_ships(tabella_attacco, tabella_difesa, navi))

        #print(str(riga) + " " + str(colonna))
        #print("")

        #time.sleep(0.05)


        attack(tabella_attacco, tabella_difesa, riga, colonna)
        check_hit_and_sunk(tabella_attacco, tabella_difesa, riga, colonna)
        if check_win(tabella_attacco, tabella_difesa):
            #print("Hai vinto!")
            return conta_mosse

def loop(bot_directory):
    conta_giochi = 0
    somma_mosse = 0

    tabella_difesa = create_table(ROWS, COLUMNS, 0)
    navi = SHIPS
    execute_function(bot_directory, "place_ships", tabella_difesa, navi)


    while True:
        conta_giochi += 1

        if conta_giochi%10 == 0:
            tabella_difesa = create_table(ROWS, COLUMNS, 0)
            execute_function(bot_directory, "place_ships", tabella_difesa, navi)

        tabella_attacco = create_table(ROWS, COLUMNS, "O")

        mosse = gioco_bot(tabella_attacco, tabella_difesa, navi, bot_directory)

        somma_mosse += mosse

        #print_table(tabella_attacco)

        if conta_giochi%100 == 0:
            print(str(somma_mosse/conta_giochi) + " -   " + str(mosse)+ "   -   " + str(conta_giochi))

        #if mosse < 80:
        #    print(str(mosse)+ "  " + str(conta_giochi))
        #    return


################################################################################
#   File management
################################################################################

def execute_function(file_path, function_name, parameter1, parameter2):
    """
    Executes a specified function from a Python module file with additional parameters.

    Parameters:
    - file_path (str): The file path of the Python module (including file extension).
    - function_name (str): The name of the function to be executed.
    - parameter1: Pass this parameter to the executed function.
    - parameter2: Pass this parameter to the executed function.

    Returns:
    - Any: The result of the executed function.

    Note:
    - If the specified function is not present in the module, an appropriate message is printed.
    - Any errors during the execution of the function are caught and printed as error messages.

    Modifies:
    - Can modify the two parameters.
    """
    result = None  # Initialize result to handle cases where the function is not called

    try:
        module_path = os.path.splitext(file_path)[0].replace(os.path.sep, '.')
        module = importlib.import_module(module_path)
        function_to_execute = getattr(module, function_name, None)

        if callable(function_to_execute):
            # Call the function with the additional parameters
            result = function_to_execute(parameter1, parameter2)
            # print(f'Executed function {function_name}() in {file_path}, result: {result}')
        else:
            print(f'Function {function_name}() is not present in {file_path}')
    except Exception as e:
        print(f'Error during execution of function {function_name}() in {file_path}: {e}')

    return result

def list_files(folder):
    """
    Lists files in the specified folder.

    Parameters:
    - folder (str): The path to the folder.

    Returns:
    - list: A list of filenames in the folder.

    Note:
    - If the folder does not exist, an appropriate message is printed, and an empty list is returned.
    - Any other errors during the operation are caught, and an empty list is returned.
    """
    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        return files
    except FileNotFoundError:
        print(f"The folder '{folder}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


################################################################################
#   MAIN
################################################################################

if __name__ == "__main__":



    """
    print('\u25A3')

    print(default_symbols.hit)
    print(config_symbols.hit)
    print(" ")
    retrive_config()
    print(default_symbols.hit)
    print(config_symbols.hit)
    """



    retrive_config()
    
    print_start()
    
    gamemode = input_gamemode()
    
    play_gamemode(gamemode)


    input("Pres ENTER to close....")


    











    
    """print(list_files("Bots"))

    file = "Bots\\NickBot.py"

    print(execute_function(file, "take_shot", create_table(10,10,"O"), SHIPS))"""

    #print(bot_directory)

    """tabella_attacco = create_table(ROWS, COLUMNS, "O")
    tabella_difesa = create_table(ROWS, COLUMNS, 0)
    navi = SHIPS

    posiziona_navi(tabella_difesa, navi)

    print_table(tabella_difesa)
    print("")

    gioco_bot(tabella_attacco, tabella_difesa, navi)

    #game(tabella_attacco, tabella_difesa)

    print_table(tabella_attacco)"""

    #loop(bot_directory)

    #print_table(generate_net(ROWS, COLUMNS, 3))
    #input("Finito")


    """
    TEST THE IMPORT LIB

    attack_table = create_table(ROWS, COLUMNS, "O")

    remaining_ships = SHIPS

    print("risultato.... " + str(execute_function("prova.py", "modifica", attack_table, remaining_ships)))

    print(remaining_ships)
    
    """


