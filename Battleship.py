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
import keyboard
import pygame
import sys
from dotenv import load_dotenv

pygame.init()

random_bot_ship_placer = "Bots\\RandomBot.py"
NUMBER_OF_DIGITS = 4

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
    global SHIPS, ROWS, COLUMNS, bots_folder

    # Load environment variables from .env file
    load_dotenv("config.env")

    # Access variables using os.getenv
    ROWS = int(os.getenv("rows"))
    COLUMNS = int(os.getenv("columns"))
    bots_folder = os.getenv("bots_folder")
    SHIPS = list(map(int, os.getenv("ships").split(',')))

    print(type(ROWS))

    config_symbols.unknown = str(os.getenv("symbol_unknown"))
    config_symbols.miss = str(os.getenv("symbol_miss"))
    config_symbols.hit = str(os.getenv("symbol_hit"))
    config_symbols.sunk = str(os.getenv("symbol_sunk"))

    print(config_symbols.miss)
    print(config_symbols.hit)


################################################################################
#   Classes
################################################################################

class Attack_board:
    def __init__(self, board, remaining_ships):
        self.board = board
        self.rows = self.Rows()
        self.columns = self.Columns()
        self.remaining_ships = remaining_ships
    
    def Rows(self):
        return len(self.board)
    
    def Columns(self):
        return len(self.board[0])


class Ship_positioning_board:
    def __init__(self, board):
        self.board = board
        self.rows = self.Rows()
        self.columns = self.Columns()
        self.ships = self.get_ships()
    
    def Rows(self):
        return len(self.board)
    
    def Columns(self):
        return len(self.board[0])
    
    def get_ships(self):
        """
        Retrieves the number of ships in the table.

        Parameters:
        - table (list): The table representing the positions of ships, where 0 denotes an empty position.

        Returns:
        - list: A list containing the number of ships in the table.
        """
        number_of_ships = max(max(self, key=max))
        ship_counts = []

        for num in range(number_of_ships):
            ship_counts.append(count_element_in_table(self, num + 1))

        return ship_counts
    
    def clear_board(self):
        self.board = [[0 for j in range(self.columns)] for i in range(self.rows)]

    def generate_random_board(self, ships):
        self.clear_board()

        ship_number = 0
        for length in ships:
            ship_number += 1
            placed = False
            while not placed:
                orientation = random.choice(['horizontal', 'vertical'])
                if orientation == 'horizontal':
                    column = random.randint(0, self.columns - length)
                    row = random.randint(0, self.rows-1)
                    if all(self.board[row][column + i] == 0 for i in range(length)):
                        for i in range(length):
                            self.board[row][column + i] = ship_number
                        placed = True
                else:
                    column = random.randint(0, self.columns-1)
                    row = random.randint(0, self.rows - length)
                    if all(self.board[row + i][column] == 0 for i in range(length)):
                        for i in range(length):
                            self.board[row + i][column] = ship_number
                        placed = True

    




################################################################################
#   GUI functions
################################################################################

def print_start():
    name = """
                            $$$$$$$\\             $$\\     $$\\     $$\\                     $$\\       $$\\           
                            $$  __$$\\            $$ |    $$ |    $$ |                    $$ |      \\__|          
 $$$$$$\\  $$\\   $$\\         $$ |  $$ | $$$$$$\\ $$$$$$\\ $$$$$$\\   $$ | $$$$$$\\   $$$$$$$\\ $$$$$$$\\  $$\\  $$$$$$\\  
$$  __$$\\ $$ |  $$ |$$$$$$\\ $$$$$$$\\ | \\____$$\\\\_$$  _|\\_$$  _|  $$ |$$  __$$\\ $$  _____|$$  __$$\\ $$ |$$  __$$\\ 
$$ /  $$ |$$ |  $$ |\\______|$$  __$$\\  $$$$$$$ | $$ |    $$ |    $$ |$$$$$$$$ |\\$$$$$$\\  $$ |  $$ |$$ |$$ /  $$ |
$$ |  $$ |$$ |  $$ |        $$ |  $$ |$$  __$$ | $$ |$$\\ $$ |$$\\ $$ |$$   ____| \\____$$\\ $$ |  $$ |$$ |$$ |  $$ |
$$$$$$$  |\\$$$$$$$ |        $$$$$$$  |\\$$$$$$$ | \\$$$$/  \\$$$$  |$$ |\\$$$$$$$\\ $$$$$$$  |$$ |  $$ |$$ |$$$$$$$  |
$$  ____/  \\____$$ |        \\_______/  \\_______|  \\____/  \\____/ \\__| \\_______|\\_______/ \\__|  \\__|\\__|$$  ____/ 
$$ |      $$\\   $$ |                                                                                   $$ |      
$$ |      \\$$$$$$  |                                                                                   $$ |      
\\__|       \\______/                                                                                    \\__|      

beta version                                                                                        by Nick806
"""
    print(name)

def input_gamemode():
    modes = """

Select a game mode [1-5]:

1) Uman gamepay with random bot ship positioning
2) Step-by-step Bot gameplay with random bot ship positioning (you can choose the bot that will play)
3) Automatic and loop Bot gamepay with random bot ship positioning (you can choose the bot that will play)
4) Automatic and loop Bot gamepay with random bot ship positioning, but return the max and the min move position(you can choose the bot that will play)
5) Step-by-step Bot gameplay with inputed ship positioning table (you can choose the bot that will play)

Gamemode n°... """
    return input(modes)

def play_gamemode(gamemode):

    gamemode = int(gamemode)

    if gamemode == 1:
        gamemode1()

    elif gamemode == 2:
        gamemode2()

    elif gamemode == 3:
       gamemode3()

    elif gamemode == 4:
       gamemode4()
    
    elif gamemode == 5:
       gamemode5()

def select_a_bot(bots_folder, message):

    bots = list_files(bots_folder)

    for num,bot in enumerate(bots):
        print(str(num) + " - " + bot)

    index = int(input("Insert the number that correspond to the bot " + message + "..."))
    while index<0 or index>(len(bots)-1):
        print("Input non possible... retry")
        index = int(input("Insert the number that correspond to the bot " + message + "..."))

    return bots[index]

def table_to_str(table):
    string = ""
    string += str(len(table))
    string += ";"
    string += str(len(table[0]))

    for rows in table:
        for element in rows:
            string += ";"
            string += str(element)
    
    return string

def str_to_table(string):
    list = string.split(";")
    
    rows = int(list[0])
    columns = int(list[1])

    table = create_table(rows, columns, 0)

    for r in range(rows):
        for c in range(columns):
            table[r][c] = int(list[(r)*columns + c+2])
    
    return table


################################################################################
#   Pygame
################################################################################

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Funzione per inizializzare la griglia
def initialize_grid(rows, cols):
    colors = [[WHITE] * cols for _ in range(rows)]
    symbols = [['' for _ in range(cols)] for _ in range(rows)]
    return colors, symbols

def initialize_color(rows, cols):
    colors = [[WHITE] * cols for _ in range(rows)]
    return colors

def initialize_symbols(rows, cols):
    symbols = [['' for _ in range(cols)] for _ in range(rows)]
    return symbols

# Funzione per disegnare la griglia
def draw_grid(rows, cols, CELL_SIZE, screen, colors, symbols, WIDTH, HEIGHT):
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, colors[row][col], rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Aggiungi bordo nero alle celle
            font = pygame.font.Font(None, 36)
            text = font.render(symbols[row][col], True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    
    # Disegna le linee orizzontali
    for row in range(rows + 1):
        pygame.draw.line(screen, BLACK, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 2)

    # Disegna le linee verticali
    for col in range(cols + 1):
        pygame.draw.line(screen, BLACK, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT), 2)

def get_cell_input(table, message):
    # Dimensioni della finestra e della griglia
    GRID_SIZE = (len(table), len(table[0]))  # Imposta il numero di righe e colonne
    CELL_SIZE = 600 // max(GRID_SIZE)  # Adatta la dimensione delle celle in base al numero di righe o colonne

    # Creazione della finestra
    rows, cols = GRID_SIZE
    WIDTH, HEIGHT = CELL_SIZE * cols, CELL_SIZE * rows
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # Aggiunta di spazio per la stringa
    pygame.display.set_caption("py-Battleship")

    # Inizializzazione dei colori e dei simboli per ogni cella
    colors, symbols = initialize_grid(rows, cols)

    for index1,row in enumerate(table):
        for index2,item in enumerate(row):
            if item == default_symbols.hit:
                colors[index1][index2] = RED
            elif item == default_symbols.miss:
                colors[index1][index2] = BLUE
            elif item == default_symbols.sunk:
                colors[index1][index2] = GREEN
            elif item == default_symbols.unknown:
                colors[index1][index2] = WHITE

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Cambia il colore e il simbolo della cella quando il mouse ci passa sopra
                mouse_x, mouse_y = event.pos
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                return row+1, col+1
            elif event.type == pygame.MOUSEMOTION:
                # Cambia il colore e il simbolo della cella quando il mouse ci passa sopra
                mouse_x, mouse_y = event.pos
                col = mouse_x // CELL_SIZE
                row = mouse_y // CELL_SIZE
                symbols = initialize_symbols(rows, cols)
                if 0 <= row < rows and 0 <= col < cols:
                    symbols[row][col] = "X"

        # Disegna la griglia
        screen.fill(WHITE)
        draw_grid(rows, cols, CELL_SIZE, screen, colors, symbols, WIDTH, HEIGHT)

        # Disegna la stringa nella parte inferiore
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 25))
        screen.blit(text, text_rect)

        # Aggiorna la finestra
        pygame.display.flip()



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


def over_possible_combination(rows, columns, ships):
    over = 1
    for ship in ships:
        over *= ((rows+1-ships[0]) * columns) + ((columns+1-ships[0]) * rows)
    return over

def max_possible_combination(table, ships):

    #TODO da completare

    rows = len(table)
    columns = len(table[0])

    if len(ships) == 1:

                #orizzontal                 #vertical
        return ((rows+1-ships[0]) * columns) + ((columns+1-ships[0]) * rows)


################################################################################
#   Section with different game modes
################################################################################

def gamemode1():
    ship_positioning_table = get_function(random_bot_ship_placer,"place_ships")(ROWS, COLUMNS, SHIPS)
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
    move = 0

    ships = SHIPS
    while True:
        print_attack(attack_table)
        
        move += 1
        print("Moove number " + str(move))
        remaining_ships = get_remaining_ships(attack_table, ship_positioning_table, ships)
        print("Remaining ships: " + str(remaining_ships))

        """while True:
            try:
                row = int(input("Row: "))
                column = int(input("Column: "))
                # da consirerare anche il caso in cui il range è esterno e il numero inserito non corrisponde
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue  # Go back to the start of the loop if the input is not valid

            break  # Exit the loop if the input is valid"""

        row , column = get_cell_input(attack_table, "Remaining ships: " + str(remaining_ships))

        attack(attack_table, ship_positioning_table, row, column)
        check_hit_and_sunk(attack_table, ship_positioning_table, row, column)
        
        if check_win(attack_table, ship_positioning_table):
            print_attack(attack_table)
            print("You won!")
            get_cell_input(attack_table, "YOU WON!     Moves:" + str(move))
            print("Table: " + table_to_str(ship_positioning_table))
            return

def gamemode2():
    ship_positioning_table = get_function(random_bot_ship_placer,"place_ships")(ROWS, COLUMNS, SHIPS)

    bot_directory =os.path.join(bots_folder, select_a_bot(bots_folder, ""))

    attack_table = create_table(ROWS, COLUMNS, "O")

    bot_attack_function = get_function(bot_directory,"take_shot")

    move = 0
    while True:
        print_attack(attack_table)
        
        move += 1
        print("Moove number " + str(move))

        remaining_ships = get_remaining_ships(attack_table, ship_positioning_table, SHIPS)
        print("Remaining ships: " + str(remaining_ships))

        row, column = bot_attack_function(attack_table, remaining_ships)

        print ("Row: " + str(row) + "   Column: " + str(column))

        input("Press ENTER to step")

        print(" ")


        attack(attack_table, ship_positioning_table, row, column)
        check_hit_and_sunk(attack_table, ship_positioning_table, row, column)
        
        if check_win(attack_table, ship_positioning_table):
            print_attack(attack_table)
            print("You won! (" + str(move) + " moves)")
            return

def gamemode3():
    count_games = 0
    count_moves = 0

    bot_directory =os.path.join(bots_folder, select_a_bot(bots_folder, ""))
    
    bot_random_place_ship_function = get_function(random_bot_ship_placer,"place_ships")
    bot_attack_function = get_function(bot_directory,"take_shot")

    while True:
        count_games += 1

        ship_positioning_table = bot_random_place_ship_function(ROWS, COLUMNS, SHIPS)
        ships = SHIPS

        attack_table = create_table(ROWS, COLUMNS, "O")
        

        move = 0
        while True:            
            move += 1
            remaining_ships = get_remaining_ships(attack_table, ship_positioning_table, ships)
            row, column = bot_attack_function(attack_table, remaining_ships)

            attack(attack_table, ship_positioning_table, row, column)
            check_hit_and_sunk(attack_table, ship_positioning_table, row, column)
            
            if check_win(attack_table, ship_positioning_table):
                break

        count_moves += move

        average = "{:.{}f}".format(count_moves/count_games, NUMBER_OF_DIGITS)
        
        print("'S' for stop! - Average moves: " + average + "  -  Moves this game: " + str(move)+ "  -  Number of games: " + str(count_games))
        
        add_line_to_file("Average moves: " + average + "  -  Moves this game: " + str(move)+ "  -  Number of games: " + str(count_games), "data.txt")
        
        if keyboard.is_pressed('s'):
            break

def gamemode4():
    count_games = 0
    count_moves = 0

    max_number_of_moves = 0
    max_moves_ship_positioning_table = []

    min_number_of_moves = ROWS*COLUMNS
    min_moves_ship_positioning_table = []

    bot_directory =os.path.join(bots_folder, select_a_bot(bots_folder, ""))

    bot_random_place_ship_function = get_function(random_bot_ship_placer,"place_ships")
    bot_attack_function = get_function(bot_directory,"take_shot")

    while True:
        count_games += 1

        ship_positioning_table = bot_random_place_ship_function(ROWS, COLUMNS, SHIPS)
        
        ships = SHIPS

        attack_table = create_table(ROWS, COLUMNS, "O")

        move = 0
        while True:            
            move += 1
            remaining_ships = get_remaining_ships(attack_table, ship_positioning_table, ships)
            row, column = bot_attack_function(attack_table, remaining_ships)

            attack(attack_table, ship_positioning_table, row, column)
            check_hit_and_sunk(attack_table, ship_positioning_table, row, column)
            
            if check_win(attack_table, ship_positioning_table):
                break
        
        if move > max_number_of_moves:
            max_number_of_moves = move
            max_moves_ship_positioning_table = ship_positioning_table
        
        if move < min_number_of_moves:
            min_number_of_moves = move
            min_moves_ship_positioning_table = ship_positioning_table

        count_moves += move

        average = "{:.{}f}".format(count_moves/count_games, NUMBER_OF_DIGITS)
        
        print("'S' for stop! - Average moves: " + average + "  -  Moves this game: " + str(move)+ "  -  Number of games: " + str(count_games)+ "  -  Max moves: " + str(max_number_of_moves)+ "  -  Min moves: " + str(min_number_of_moves))
        
        if keyboard.is_pressed('s'):
            print("Max moves: " + str(max_number_of_moves))
            print_table(max_moves_ship_positioning_table)
            print("Table unicode:" + table_to_str(max_moves_ship_positioning_table))
            print(" ")
            print("Min moves: " + str(min_number_of_moves))
            print_table(min_moves_ship_positioning_table)
            print("Table unicode:" + table_to_str(min_moves_ship_positioning_table))
            break

def gamemode5():

    ship_positioning_table = str_to_table(input("Enter the input string for the ship positioning table:"))

    print_table(ship_positioning_table)
    print("")

    bot_directory =os.path.join(bots_folder, select_a_bot(bots_folder, ""))

    attack_table = create_table(ROWS, COLUMNS, "O")

    bot_attack_function = get_function(bot_directory,"take_shot")

    move = 0
    while True:
        print_attack(attack_table)
        
        move += 1
        print("Moove number " + str(move))

        remaining_ships = get_remaining_ships(attack_table, ship_positioning_table, SHIPS)
        print("Remaining ships: " + str(remaining_ships))

        row, column = bot_attack_function(attack_table, remaining_ships)

        print ("Row: " + str(row) + "   Column: " + str(column))

        input("Press ENTER to step")

        print(" ")


        attack(attack_table, ship_positioning_table, row, column)
        check_hit_and_sunk(attack_table, ship_positioning_table, row, column)
        
        if check_win(attack_table, ship_positioning_table):
            print_attack(attack_table)
            print("You won! (" + str(move) + " moves)")
            return

#TODO Write this in english
        
def gioco_bot(tabella_attacco, tabella_difesa, navi, bot_directory):

    bot_attack_function = get_function(bot_directory,"take_shot")

    conta_mosse = 0

    while True:
        conta_mosse += 1

        riga, colonna = bot_attack_function(tabella_attacco, get_remaining_ships(tabella_attacco, tabella_difesa, navi))

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

    bot_random_place_ship_function = get_function(random_bot_ship_placer,"place_ships")

    tabella_difesa = bot_random_place_ship_function(ROWS, COLUMNS, navi)
    navi = SHIPS


    while True:
        conta_giochi += 1

        if conta_giochi%10 == 0:
            tabella_difesa = bot_random_place_ship_function(ROWS, COLUMNS, navi)

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

def get_function(file_path, function_name):
    """
    Dynamically imports a module from a file and retrieves the specified function.

    Parameters:
    - file_path (str): The path to the Python file containing the module.
    - function_name (str): The name of the function to retrieve.

    Returns:
    - the function of the file

    If the function or module is not found, an error message is printed, and the program exits.
    """
    try:
        module_path = os.path.splitext(file_path)[0].replace(os.path.sep, '.')
        module = importlib.import_module(module_path)
        function_to_execute = getattr(module, function_name, None)

        if callable(function_to_execute):
            return function_to_execute           
        else:
            print(f'Function {function_name}() is not present in {file_path}')
            exit()
    except Exception as e:
        print(f'Error during execution of function {function_name}() in {file_path}: {e}')
        exit()

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

def add_line_to_file(text, full_path):

    # Open the file in append mode or create the file if it doesn't exist
    with open(full_path, 'a+') as file:
        # Move to the beginning of the file (in case it already exists)
        file.seek(0)

        # Check if the file is empty
        is_empty = not bool(file.read(1))

        # If the file is not empty, add a new line
        if not is_empty:
            file.write('\n')

        # Add the line with the input text
        file.write(text)


################################################################################
#   MAIN
################################################################################

attack_board = Attack_board(create_table(ROWS, COLUMNS, "O"))

print_table(attack_board.board)
print(attack_board.rows)
print(attack_board.columns)

if __name__ == "__main__":
        
    
    """
    retrive_config()

    while True:

        pygame.init()
        
        print_start()
        
        gamemode = input_gamemode()
        
        play_gamemode(gamemode)

        pygame.quit()

        input("Pres ENTER to close....")

        """

    










    #print(over_possible_combination(int(input("Rows: ")), int(input("Columns: ")), [2,2,2,2,3,3,3,4,4,5]))
    
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


