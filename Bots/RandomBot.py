import random
import time
import os
import importlib


# fondamental function

def take_shot(attack_table, remaining_ships):
    legal_moves = legal_moves_list(attack_table)
    mossa = random.randint(0, len(legal_moves)-1)

    row = legal_moves[mossa][0]
    column = legal_moves[mossa][1]

    return row, column

def place_ships(tabella, navi):
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


# bot secondary functions

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
