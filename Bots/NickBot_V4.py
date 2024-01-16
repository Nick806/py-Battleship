import random

# fondamental function

def take_shot(attack_table, remaining_ships):
    legal_moves = legal_moves_list(attack_table)

    print("ciao")



    list_X = table_to_list(attack_table, "X")

    if list_X != []:

        for coordinate in list_X:

            row = coordinate[0]
            column = coordinate[1]

            surrounding = surrounding_coordinates(row, column)
            surrounding_X = common_elements(surrounding, list_X)
            
            if surrounding_X != []:

                for element in surrounding_X:
                    print(element)
                    if element [0] == row: #orizzontal
                        r = row
                        c = column
                        while True: #to the left
                            c-=1
                            if attack_table[r-1][c-1] == "O":
                                return r, c
                            elif attack_table[r-1][c-1] == "Y" or attack_table[r-1][c-1] == "A" or c <= 0:
                                break
                        
                        c = column
                        while True: #to the right
                            c+=1
                            if attack_table[r-1][c-1] == "O":
                                return r, c
                            elif attack_table[r-1][c-1] == "Y" or attack_table[r-1][c-1] == "A" or c >= len(attack_table[0]):
                                break


                    elif element [1] == column: #vertical
                        r = row
                        c = column
                        while True: #up
                            r-=1
                            if attack_table[r-1][c-1] == "O":
                                return r, c
                            elif attack_table[r-1][c-1] == "Y" or attack_table[r-1][c-1] == "A" or r <= 0:
                                break
                        
                        r = row
                        while True: #down
                            r+=1
                            if attack_table[r-1][c-1] == "O":
                                return r, c
                            elif attack_table[r-1][c-1] == "Y" or attack_table[r-1][c-1] == "A" or r >= len(attack_table):
                                break

        for coordinate in list_X:
            coordinate1 = coordinate[0]
            coordinate2 = coordinate[1]

            surrounding = surrounding_coordinates(coordinate1, coordinate2)
            move = common_elements(surrounding, legal_moves)

            if len(move) > 0:
                row = move[0][0]
                column = move[0][1]
                return row, column
            
    return find_maximum_coordinates(calculate_probability_table(attack_table, remaining_ships))

def place_ships(board, ships):
    rows = len(board) - 1
    columns = len(board[0]) - 1

    ship_number = 0
    for length in ships:
        ship_number += 1
        placed = False
        while not placed:
            orientation = random.choice(['horizontal', 'vertical'])
            if orientation == 'horizontal':
                column = random.randint(0, columns - length)
                row = random.randint(0, rows)
                if all(board[row][column + i] == 0 for i in range(length)):
                    for i in range(length):
                        board[row][column + i] = ship_number
                    placed = True
            else:
                column = random.randint(0, columns)
                row = random.randint(0, rows - length)
                if all(board[row + i][column] == 0 for i in range(length)):
                    for i in range(length):
                        board[row + i][column] = ship_number
                    placed = True


# basic functions
                    
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


# bot secondary functions

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
