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

# global

COLUMNS = 10
ROWS = 10

SHIPS = [2,2,2,2,3,3,3,4,4,5]
# each number corresponds to the length of a ship


import random
import time


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
#   Section with game functions
################################################################################

def game(attack_table, defense_table):
    """
    Initiates and manages the gameplay loop.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.
    - defense_table (list): The table representing the positions of ships, where 0 denotes an empty position.

    Note:
    - The function manages the player's turns, taking input for row and column to perform an attack.
    - It then updates the attack table and checks for hits and sunk ships.
    - The game continues until the player wins.
    """
    while True:
        print_table(attack_table)

        while True:
            try:
                row = int(input("Row: "))
                column = int(input("Column: "))
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue  # Go back to the start of the loop if the input is not valid

            break  # Exit the loop if the input is valid

        attack(attack_table, defense_table, row, column)
        check_hit_and_sunk(attack_table, defense_table, row, column)
        
        if check_win(attack_table, defense_table):
            print("You won!")
            return



def gioco_bot(tabella_attacco, tabella_difesa, navi):

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


        riga, colonna = my_bot_4(tabella_attacco, get_remaining_ships(tabella_attacco, tabella_difesa, navi))

        #print(str(riga) + " " + str(colonna))
        #print("")

        #time.sleep(0.05)


        attack(tabella_attacco, tabella_difesa, riga, colonna)
        check_hit_and_sunk(tabella_attacco, tabella_difesa, riga, colonna)
        if check_win(tabella_attacco, tabella_difesa):
            #print("Hai vinto!")
            return conta_mosse


def loop():
    conta_giochi = 0
    somma_mosse = 0

    tabella_difesa = create_table(ROWS, COLUMNS, 0)
    navi = SHIPS
    posiziona_navi(tabella_difesa, navi)


    while True:
        conta_giochi += 1

        if conta_giochi%10 == 0:
            tabella_difesa = create_table(ROWS, COLUMNS, 0)
            posiziona_navi(tabella_difesa, navi)

        tabella_attacco = create_table(ROWS, COLUMNS, "O")

        mosse = gioco_bot(tabella_attacco, tabella_difesa, navi)

        somma_mosse += mosse

        #print_table(tabella_attacco)

        if conta_giochi%100 == 0:
            print(str(somma_mosse/conta_giochi) + " -   " + str(mosse)+ "   -   " + str(conta_giochi))

        #if mosse < 80:
        #    print(str(mosse)+ "  " + str(conta_giochi))
        #    return


################################################################################
#   BOTS
################################################################################			

def posiziona_navi(tabella, navi):
    righe = len(tabella)-1
    colonne = len(tabella[0])-1

    numero_nave = 0
    for lunghezza in navi:
        numero_nave += 1
        posizionata = False
        while not posizionata:
            orientamento = random.choice(['orizzontale', 'verticale'])
            if orientamento == 'orizzontale':
                colonna = random.randint(0, colonne - lunghezza)
                riga = random.randint(0, righe)
                if all(tabella[riga][colonna + i] == 0 for i in range(lunghezza)):
                    for i in range(lunghezza):
                        tabella[riga][colonna + i] = numero_nave
                    posizionata = True
            else:
                colonna = random.randint(0, colonne)
                riga = random.randint(0, righe - lunghezza)
                if all(tabella[riga + i][colonna] == 0 for i in range(lunghezza)):
                    for i in range(lunghezza):
                        tabella[riga + i][colonna] = numero_nave
                    posizionata = True



#circa 97.73176 tentativi in 21000 partite
def my_bot(tabella_attacco, navi_rimanenti):
    lista_mosse_legali = legal_moves_list(tabella_attacco)
    mossa = random.randint(0, len(lista_mosse_legali)-1)

    riga = lista_mosse_legali[mossa][0]
    colonna = lista_mosse_legali[mossa][1]

    return riga, colonna


#circa 77.907 tentativi in 20800 partite
def my_bot_2(tabella_attacco, navi_rimanenti):
    mosse_legali = legal_moves_table(tabella_attacco)
    lista_mosse_legali = legal_moves_list(tabella_attacco)

    lista_X = table_to_list(tabella_attacco, "X")

    if lista_X != 0:

        for indice in lista_X:
            indice1 = indice[0]
            indice2 = indice[1]

            intorno = surrounding_coordinates(indice1, indice2)
            mossa = common_elements(intorno, lista_mosse_legali)

            if len(mossa) > 0:
                riga = mossa[0][0]
                colonna = mossa[0][1]
                return riga, colonna


    mossa = random.randint(0, len(lista_mosse_legali)-1)

    riga = lista_mosse_legali[mossa][0]
    colonna = lista_mosse_legali[mossa][1]

    return riga, colonna


#circa 70.57 tentativi in 17700 partite
def my_bot_3(tabella_attacco, navi_rimanenti):
    tabella_mosse_legali = legal_moves_table(tabella_attacco)
    lista_mosse_legali = legal_moves_list(tabella_attacco)



    lista_X = table_to_list(tabella_attacco, "X")

    if lista_X != 0:

        for indice in lista_X:
            indice1 = indice[0]
            indice2 = indice[1]

            intorno = surrounding_coordinates(indice1, indice2)
            mossa = common_elements(intorno, lista_mosse_legali)

            if len(mossa) > 0:
                riga = mossa[0][0]
                colonna = mossa[0][1]
                return riga, colonna


    min_nave = min(navi_rimanenti)

    lista_rete = table_to_list(generate_net(len(tabella_attacco), len(tabella_attacco[0]), min_nave), 1)

    lista_mosse = common_elements(lista_rete, lista_mosse_legali)

    mossa = random.randint(0, len(lista_mosse)-1)

    riga = lista_mosse[mossa][0]
    colonna = lista_mosse[mossa][1]

    return riga, colonna


#circa 64.6 mosse in 354 partite DIVERSE
def my_bot_4(tabella_attacco, navi_rimanenti):
    tabella_mosse_legali = legal_moves_table(tabella_attacco)
    lista_mosse_legali = legal_moves_list(tabella_attacco)



    lista_X = table_to_list(tabella_attacco, "X")

    if lista_X != 0:

        for indice in lista_X:
            indice1 = indice[0]
            indice2 = indice[1]

            intorno = surrounding_coordinates(indice1, indice2)
            mossa = common_elements(intorno, lista_mosse_legali)

            if len(mossa) > 0:
                riga = mossa[0][0]
                colonna = mossa[0][1]
                return riga, colonna


    """min_nave = min(navi_rimanenti)

    lista_rete = table_to_list(generate_net(len(tabella_attacco), len(tabella_attacco[0]), min_nave), 1)

    lista_mosse = common_elements(lista_rete, lista_mosse_legali)

    mossa = random.randint(0, len(lista_mosse)-1)

    riga = lista_mosse[mossa][0]
    colonna = lista_mosse[mossa][1]"""

    return find_maximum_coordinates(calculate_probability_table(tabella_attacco, navi_rimanenti))


def find_maximum_coordinates(table):
    """
    Finds the coordinates of the maximum value in a 2D table.

    Parameters:
    - table (list): The 2D table.

    Returns:
    - tuple: The row and column coordinates (index + 1) of the maximum value in the table.
    """
    rows = len(table)
    columns = len(table[0])

    max_row_index = 0
    max_column_index = 0
    max_value = table[0][0]

    for i in range(rows):
        for j in range(columns):
            if table[i][j] > max_value:
                max_value = table[i][j]
                max_row_index = i
                max_column_index = j

    return max_row_index + 1, max_column_index + 1

def ship_area(rows, columns, row, column, length, orientation):
    """
    Returns the area occupied by a ship in a 2D table.

    Parameters:
    - rows (int): The number of rows in the table.
    - columns (int): The number of columns in the table.
    - row (int): The starting row index of the ship (index - 1).
    - column (int): The starting column index of the ship (index - 1).
    - length (int): The length of the ship.
    - orientation (int): 1 for vertical, 0 for horizontal.

    Returns:
    - list: A 2D table representing the area occupied by the ship whit ones (1), the rest of the table remain zeros (0).
    """
    table = create_table(rows, columns, 0)

    if orientation:
        # Vertical
        for x in range(length):
            table[row - 1 + x][column - 1] = 1

    else:
        # Horizontal
        for x in range(length):
            table[row - 1][column - 1 + x] = 1

    return table

def remove_duplicates(lst):
    """
    Removes duplicate elements from a list.

    Parameters:
    - lst (list): The list containing elements, some of which may be duplicates.

    Returns:
    - list: A new list containing unique elements, preserving the order of the original list.
    """
    new_list = []
    for element in lst:
        if element not in new_list:
            new_list.append(element)

    return new_list

def list_all_ship_positions(rows, columns, remaining_ships):
    """
    Lists all possible positions for the remaining ships on the game board.

    Parameters:
    - rows (int): The number of rows in the game board.
    - columns (int): The number of columns in the game board.
    - remaining_ships (list): The list of remaining ships to be placed.

    Returns:
    - list: A list containing all ship positions for the remaining ships length.
    """
    ships = remove_duplicates(remaining_ships)
    positions = []

    for length in ships:
        # Vertical positions
        for row in range(rows - length + 1):
            for col in range(columns):
                positions.append([row + 1, col + 1, length, 1])

        # Horizontal positions
        for col in range(columns - length + 1):
            for row in range(rows):
                positions.append([row + 1, col + 1, length, 0])

    return positions

def list_possible_ships(attack_table, all_ships_list):
    """
    Generates a list of possible ship positions based on the current state of attack table.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "A" denotes a hit and "Y" denotes a sunk ship.
    - all_ships_list (list): The list of all ships in the format [row, column, length, orientation].

    Returns:
    - list: A list of possible ship positions that have not been hit or sunk.
    """
    possible_ships = []

    for ship in all_ships_list:
        positioned = True
        ship_area_table = ship_area(len(attack_table), len(attack_table[0]), ship[0], ship[1], ship[2], ship[3])

        for i, row_list in enumerate(ship_area_table):
            for j, element in enumerate(row_list):
                if element:  # If it's 1, there's a ship
                    if attack_table[i][j] == "A" or attack_table[i][j] == "Y":
                        positioned = False
                        break
            if not positioned:
                break

        if positioned:
            possible_ships.append(ship)

    return possible_ships

def probability_table(rows, columns, possible_ships, remaining_ships):
    """
    Generates a probability table indicating the likelihood of ships being present in each cell.

    Parameters:
    - rows (int): The number of rows in the table.
    - columns (int): The number of columns in the table.
    - possible_ships (list): List of possible ship positions in the format [row, column, length, orientation].
    - remaining_ships (list): List of remaining ships in the format [row, column, length, orientation].

    Returns:
    - list: A 2D table representing the probability of a ship being present in each cell.
    """
    table = create_table(rows, columns, 0)

    possible_ship_lengths = [ship[2] for ship in possible_ships]
    remaining_lengths = remove_duplicates(remaining_ships)

    for lengths in remaining_lengths:
        remaining_count = remaining_ships.count(lengths)
        possible_count = possible_ship_lengths.count(lengths)

        probability = remaining_count / possible_count

        for possible_ship in possible_ships:
            if possible_ship[2] == lengths:
                ship_area_table = ship_area(rows, columns, possible_ship[0], possible_ship[1], possible_ship[2], possible_ship[3])

                for i, row_list in enumerate(ship_area_table):
                    for j, element in enumerate(row_list):
                        if element:  # If it's 1, there's a ship
                            table[i][j] += probability

    return table

def calculate_probability_table(attack_table, remaining_ships):
    """
    Calculates the probability table based on the current state of the attack table and the remaining ships.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.
    - remaining_ships (list): The list of remaining ships in the format [row, column, length, orientation].

    Returns:
    - list: A 2D table representing the probability of a ship being present in each cell.
    """
    rows = len(attack_table)
    columns = len(attack_table[0])

    return probability_table(rows, columns, list_possible_ships(attack_table, list_all_ship_positions(rows, columns, remaining_ships)), remaining_ships)

def generate_net(rows, columns, ship_size):
    """
    Generates a network pattern in a 2D table.

    Parameters:
    - rows (int): The number of rows in the table.
    - columns (int): The number of columns in the table.
    - ship_size (int): The size of the ship.

    Returns:
    - list: A 2D table with a network pattern of the specified ship size.
    """
    table = create_table(rows, columns, 0)

    for r in range(rows):
        for c in range(columns):
            if (c + r) % ship_size == 0:
                table[r][c] = 1

    return table

def common_elements(list1, list2):
    """
    Finds common elements between two lists.

    Parameters:
    - list1 (list): The first list.
    - list2 (list): The second list.

    Returns:
    - list: A list containing common elements between the two input lists.
    """
    common_elements_list = []
    for elem1 in list1:
        for elem2 in list2:
            if elem1 == elem2:
                common_elements_list.append(elem1)

    return common_elements_list

def surrounding_coordinates(x, y):
    """
    Generates a list of coordinates surrounding a given point.

    Parameters:
    - x (int): The x-coordinate.
    - y (int): The y-coordinate.

    Returns:
    - list: A list containing coordinates surrounding the input point.

    Note:
    - The function may generate coordinates that could be outside the legal boundaries.
      It is recommended to filter the output using a list of legal moves.
    """
    surroundings = [
        [x - 1, y],  # Left
        [x + 1, y],  # Right
        [x, y - 1],  # Above
        [x, y + 1]   # Below
    ]
    return surroundings

def table_to_list(table, element):
    """
    Converts a 2D table to a list of coordinates where a specified element is present.

    Parameters:
    - table (list): The 2D table.
    - element: The element to search for in the table.

    Returns:
    - list: A list containing coordinates where the specified element is present.
    """
    coordinates = []
    for index1, row in enumerate(table):
        for index2, value in enumerate(row):
            if value == element:
                coordinates.append([index1 + 1, index2 + 1])

    return coordinates

def legal_moves_table(attack_table):
    """
    Generates a table indicating legal moves for attacks.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.

    Returns:
    - list: A 2D table with legal moves marked as 1 and non-legal moves marked as 0.
    """
    legal_moves = create_table(len(attack_table), len(attack_table[0]), 0)

    for row in range(len(legal_moves)):
        for col in range(len(legal_moves[0])):
            if attack_table[row][col] == "O":
                legal_moves[row][col] = 1

    return legal_moves

def legal_moves_list(attack_table):
    """
    Generates a list of legal moves for attacks.

    Parameters:
    - attack_table (list): The table representing the state of attacks, where "O" denotes an unattacked position.

    Returns:
    - list: A list of coordinates representing legal moves.
    """
    legal_moves_tab = legal_moves_table(attack_table)
    legal_moves_list = []

    for row in range(len(legal_moves_tab)):
        for col in range(len(legal_moves_tab[0])):
            if legal_moves_tab[row][col] == 1:
                legal_moves_list.append([row + 1, col + 1])

    return legal_moves_list


################################################################################
#   MAIN
################################################################################			


if __name__ == "__main__":



    """tabella_attacco = create_table(ROWS, COLUMNS, "O")
    tabella_difesa = create_table(ROWS, COLUMNS, 0)
    navi = SHIPS

    posiziona_navi(tabella_difesa, navi)

    print_table(tabella_difesa)
    print("")

    gioco_bot(tabella_attacco, tabella_difesa, navi)

    #game(tabella_attacco, tabella_difesa)

    print_table(tabella_attacco)"""

    loop()

    #print_table(generate_net(ROWS, COLUMNS, 3))
    #input("Finito")


