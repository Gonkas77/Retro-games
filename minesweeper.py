import random

run = True
columns = 0
rows = 0
bombs = 0

while True:
    print("\nEasy: 9x9 with 10 bombs.")
    print("Medium: 16x16 with 40 bombs.")
    print("Hard: 30x16 with 99 bombs.")
    print("Custom: custom size and bomb number.")
    difficulty = input("\nChoose difficulty: ")

    match difficulty.lower():
        case "e"|"easy"|"1":
            columns = 9
            rows = 9
            bombs = 10
            break

        case "m"|"medium"|"2":
            columns = 16
            rows = 16
            bombs = 40
            break

        case "h"|"hard"|"3":
            columns = 30
            rows = 16
            bombs = 99
            break

        case "c"|"custom"|"0":
            columns = int(input("Enter the number of columns (max 100): "))
            rows = int(input("Enter the number of rows (max 100): "))
            bombs = int(input("Enter the number of bombs: "))

            if columns <= rows <= 100 and bombs < columns*rows:
                break

    print("\nInvalid difficulty! Try again.")

bomb_spaces = []
flags = bombs

revealed_spaces = 0
reveal_spaces = []

# functions

def create_board(rows, columns, bombs):
    global board
    
    board = []

    spaces = []
    for k in range(rows*columns):
        spaces.append(k)

    bomb_spaces = get_bombs(len(spaces), bombs)

    c = 0
    r = -1

    for s in range(rows*columns):

        if s % rows == 0:
            r += 1
            c = 0

        board.append([(c, r), 0, False, False])

        c += 1

    for b in bomb_spaces:
        board[b][1] = -1
        alter_surrounding_squares(get_surrounding_squares(board[b][0]), 'b')

def get_bombs(board_size, bombs):
    global bomb_spaces

    # create board with board_size spaces
    spaces = [i for i in range(board_size)]

    for b in range(bombs):
        new_bomb = random.randint(0, len(spaces)-1)
        bomb_spaces.append(spaces[new_bomb])
        spaces.pop(b)

    return bomb_spaces

def get_surrounding_squares(coordinates: tuple):
    global rows, columns

    x = coordinates[0]
    y = coordinates[1]

    c = columns
    r = rows

    if 0 < x < c-1 and 0 < y < r-1:
        type = 'm'

    elif 0 < y < r-1:
        if x == 0:
            type = 'l'
        else:
            type = 'r'

    elif 0 < x < c-1:
        if y == 0:
            type = 't'
        else:
            type = 'b'

    elif y == 0:
        if x == 0:
            type = '0'
        else:
            type = '1'

    else:
        if y == 0:
            type = '2'
        else:
            type = '3'

    x_start = x-1
    x_stop = x+1

    y_start = y-1
    y_stop = y+1

    match type:

        case 'l':
            x_start = x

        case 'r':
            x_stop = x

        case 't':
            y_start = y

        case 'b':
            y_stop = y

        case '0': # top left
            x_start = x
            y_start = y

        case '1': # top right
            x_stop = x
            y_start = y

        case '2': # bottom left
            x_start = x
            y_stop = y

        case '3': # bottom right
            x_stop = x
            y_stop = y

    return (x_start, x_stop, y_start, y_stop)

def alter_surrounding_squares(params: tuple, action: str):
    global reveal_spaces

    x_start = params[0]
    x_stop = params[1]

    y_start = params[2]
    y_stop = params[3]

    if action == 'r':
        condition = True
    elif action == 'b':
        condition = False

    for y in range(y_start, y_stop+1):
        for x in range(x_start, x_stop+1):
            index = convert_coordinates_to_index((x, y))

            if board[index][1] != -1:
                if condition: # reveal surrounding squares
                    
                    if reveal_spaces.count(index) == 0:
                        reveal_spaces.append(index)
                        if board[index][1] == 0:
                            alter_surrounding_squares(get_surrounding_squares(convert_index_to_coordinates(index)), action)

                else: # increase surrounding square numbers
                    board[index][1] += 1

def print_board():
    global board

    for s in range(len(board)):
        
        if s % rows == 0:
            print()

        character_to_print = '-'
        if board[s][2]:
            if board[s][1] != -1:
                character_to_print = board[s][1]
            else:
                character_to_print = '#'
        elif board[s][3]:
            character_to_print = 'F'

        if s == len(board)-1:
            print(f" {character_to_print}\n")
        else:
            print(f" {character_to_print}", end=" ")

def is_valid_action(action: str):
    return has_number_part(action) and has_letter_part(action)   

def has_number_part(string: str):
    return has_char_type(string, 'd')

def has_letter_part(string: str):
    return has_char_type(string, 'l')

def has_char_type(string: str, type: str):
    characters = list(string)
    for char in characters:
        if get_char_type(char) == type:
            return True
    return False

def get_char_type(character: str):
    match character:
        case 'r'|'f':
            return 'l'
        case '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9':
            return 'd'
    return ''

def print_notation():
    print("\nNotation:")
    print("space index (count from top left to bottom right) as a number starting at 0")
    print("action to perform as a letter | r = reveal space, f = place/remove flag (not capital sensitive)")

def perform_action(action: str):
    global run, revealed_spaces
    
    action = simplify_action_string(action)
    if len(action) == 0:
        return

    number_part = int(action[0])
    letter_part = action[1]
    space = board[number_part]

    if letter_part == 'r':
        if space[1] == -1:
            run = False
            print("\nYou lost... You stepped on a bomb!")
        elif space[1] == 0:
            reveal_surrounding_squares(number_part)
        else:
            space[2] = True
            revealed_spaces += 1
    elif letter_part == 'f':
        if (not space[2]) and flags > 0:
            space[3] = not space[3]
    else:
        print_notation()


def simplify_action_string(action: str):

    characters = list(action.lower())

    number_part = ""
    letter_part = ""

    for char in characters:
        if get_char_type(char) == 'd':
            number_part += char
        else:
            letter_part += char

    while len(number_part) > 1 and list(number_part)[0] == 0:
        number_part.removeprefix('0')

    if int(number_part) > len(board)-1:
        return ()

    return (number_part, letter_part)

def reveal_surrounding_squares(square_index: int):
    global revealed_spaces
    
    params = get_surrounding_squares(convert_index_to_coordinates(square_index))
    alter_surrounding_squares(params, 'r')

    for s in reveal_spaces:
        board[s][2] = True
        revealed_spaces += 1
    reveal_spaces.clear()

def convert_index_to_coordinates(index: int):

    y = index // rows
    x = index - y*rows

    return (x, y)

def convert_coordinates_to_index(coordinates: tuple):

    x = coordinates[0]
    y = coordinates[1]

    return y*columns+x

# main

create_board(rows, columns, bombs)

while (run):
    
    print_board()
    print("Number of flags left: " + str(flags))
    print("Total number of bombs: " + str(bombs))
    
    player_action = input("Enter your action (type \"h\" for help with notation): ")

    match player_action.lower():
        case "s"|"stop"|"leave"|"terminate"|"end":
            run = False
            print()
            break

    if not is_valid_action(player_action):
        print_notation()
    else:
        perform_action(player_action)

        # check if player wins
        if revealed_spaces == len(board) - bombs:
            run = False
            for b in bomb_spaces:
                board[b][2] = True

            print_board()
            print("\nYou won! All bombs were cleared!")