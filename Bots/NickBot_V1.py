import random


# fondamental function

def take_shot(attack_table, remaining_ships):
    lista_mosse_legali = legal_moves_list(attack_table)

    lista_X = table_to_list(attack_table, "X")

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

