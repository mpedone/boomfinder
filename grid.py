import random
import constants
import sys

def bomb_placement(width, height, bomb_count, row, col):
    """
    Docstring for bomb_placement
    
    :param width: width of the board
    :param height: height of the board
    :param bomb_count: number of bombs to be placed
    :param row: the row of the player's first move
    :param col: the column of the player's first move

    Output: the bomb grid

    This function is called when the user makes their first selection. It builds a list of all possible moves, pops the user's selection out of it, and selects a number randomly from this list. It then creates a grid the same dimensions as the game board, but all zeros, and then sets each bomb location to 1 
    """
    game_board_x = list(range(height))
    game_board_y = list(range(width))
    board = [(x, y) for x in game_board_x for y in game_board_y]
    selection = board.index((row, col))
    sel = board.pop(selection)

    bombs = random.sample(board, bomb_count)
    bomb_grid = [[0 for x in range(width)] for y in range(height)]
    for bomb in bombs:
        bomb_grid[bomb[0]][bomb[1]] = 1
    return bomb_grid

def print_grid(grid):
    width = len(grid[0])
    first_row_numbers = list(range(width))
    first_row = "   "
    first_row += " ".join([str(n+1) for n in first_row_numbers])

    print(first_row)
    for i in range(len(grid)):
        grid_row = ""
        if i < 9:
            grid_row = " "
        idx = i+1
        grid_row += str(idx)
        for j in range(len(grid[i])):
            grid_row += f" {str(grid[i][j])}"
        print(grid_row)

def calc_dist(width, height, bomb_grid):
    dist_grid = [[0 for _ in range(width)] for _ in range(height)]
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for row in range(len(bomb_grid)):
        for col in range(len(bomb_grid[row])):
            if bomb_grid[row][col] == 1:
                dist_grid[row][col] += 9
            else:
                for dir in directions:
                    new_row = row + dir[0]
                    new_col = col + dir[1]
                    if new_row < 0 or new_row >= width or new_col < 0 or new_col >= width:
                        continue
                    else:
                        dist_grid[row][col] += bomb_grid[new_row][new_col]
            if dist_grid[row][col] == 0:
                dist_grid[row][col] = " "
            elif dist_grid[row][col] == 9:
                dist_grid[row][col] = "*"
    return dist_grid

def update_grid(base_grid, dist_grid, user_row, user_col):
    status = 1
    if base_grid[user_row][user_col] == "F":
        pass
    elif dist_grid[user_row][user_col] == "*":
        check_flags(base_grid, dist_grid)
        print_grid(base_grid)
        # print_grid(dist_grid)
        print("You hit a BOOM! Game over!")
        status = 0
    # elif dist_grid[user_row][user_col] == " ":
    #     base_grid[user_row][user_col] = dist_grid[user_row][user_col]
    #     clear_region(user_row, user_col, base_grid, dist_grid)
        # auto_clear(user_row, user_col, base_grid, dist_grid)
    else:
        base_grid[user_row][user_col] = dist_grid[user_row][user_col]
        # if base_grid[user_row][user_col] == " ":
        #     auto_clear(user_row, user_col, base_grid, dist_grid)
    return base_grid, status

def intialize_grid(board_width, board_height):
    print("Let's Find Some BOOMS!")
    width_entry = "none"
    height_entry = "none"
    bombs_entry = "none"
    
    while not width_entry.isnumeric() and width_entry != "":
        width_entry = input("Set the board width (leave blank for default): ")
        if width_entry == "h":
            instructions()
            continue
        if width_entry == "q":
            sys.exit(1)
    if width_entry.isnumeric():
        if int(width_entry) < 3:
            print("Board too small, defaulting to 3")
            board_width = 3
        elif int(width_entry) > constants.MAX_BOARD_WIDTH:
            print(f"Board too wide, limiting to {constants.MAX_BOARD_WIDTH}.")
            board_width = constants.MAX_BOARD_WIDTH
        else:
            board_width = int(width_entry)
    else:
        print(f"Using defalut ({board_width})")

    while not height_entry.isnumeric() and height_entry != "":  
        height_entry = input("Set the board height (leave blank for default): ")
        if height_entry == "h":
            instructions()
            continue
        if height_entry == "q":
            sys.exit(1)
    if height_entry.isnumeric():
        if int(height_entry) < 3:
            print("Board too small, defaulting to 3.")
            board_height = 3
        elif int(height_entry) > constants.MAX_BOARD_HEIGHT:
            print(f"Board too tall. Limiting to {constants.MAX_BOARD_HEIGHT}.")
            board_height = constants.MAX_BOARD_HEIGHT
        else:
            board_height = int(height_entry)
    else:
        print(f"Using defalut ({board_height})")

    while not bombs_entry.isnumeric() and bombs_entry != "":
        bombs_entry = input("How many BOOMS? (leave blank for auto): ")
        if bombs_entry == "h":
            instructions()
            continue
        if bombs_entry == "q":
            sys.exit(1)
    if not bombs_entry.isnumeric():
        bombs_raw = (0.00708274 * (board_width * board_height)**1.53966) + 3.85371
        number_of_bombs = int(bombs_raw)
        print(f"BOOMS calculated automatically: {number_of_bombs}")
    elif int(bombs_entry) > (board_width * board_height) - 1:
        print(f"Too many BOOMS! Limiting to {(board_width * board_height) - 1}")
        number_of_bombs = (board_width * board_height) - 1
    elif int(bombs_entry) < 0:
        print("Too few BOOMS! Limiting to 1.")
        number_of_bombs = 1
    else:
        number_of_bombs = int(bombs_entry)
    number_of_safes = board_width * board_height - number_of_bombs
    
    return board_width, board_height, number_of_bombs, number_of_safes

def first_move(player_row, player_col, board_width, board_height, number_of_bombs, base_grid, status=1, moves=0):
    """
    Docstring for first_move
    
    :param row: Row selection
    :param col: Column selection

    This is the function for the first square reveal of the game. This is a unique move because the bombs are not placed until the user selects a square to reveal. This is mainly to guarantee the game actually starts, but also becuase that's how I've always assumed the Windows game did it.
    """
    bomb_grid = bomb_placement(board_width, board_height, number_of_bombs, player_row, player_col)
    dist_grid = calc_dist(board_width, board_height, bomb_grid)
    base_grid, status = update_grid(base_grid, dist_grid, player_row, player_col)
    moves += 1
    cleared = (board_width * board_height) - grid_count(base_grid)
    return base_grid, status, dist_grid, moves, cleared

def square_select(base_grid, selection):
    valid_input = "start"
    valid = 0

    while valid_input != "":
        row_err = ""
        col_err = ""
        # print(valid_input)
        user_input = input("Select a square: ")
        if input == "":
            continue
        if user_input[0].lower() == "q":
            sys.exit(1)
        if "," not in user_input:
            print("Please format entry as 'row, col'.")
            continue
        row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
        if not row_input.isnumeric() or int(row_input)-1 not in range(0, len(base_grid)):
            row_err = f"Row must be a number between 1 and {len(base_grid)}. "
        if not col_input.isnumeric() or int(col_input)-1 not in range(0, len(base_grid[0])):
            col_err = f"Col must be a number between 1 and {len(base_grid)}."
        # print(row_err + col_err)
        if row_err + col_err == "":
            row_input = int(row_input)-1
            col_input = int(col_input)-1
            if selection == "f":
                if base_grid[row_input][col_input] not in ["_", "F"]:
                    print("Please select an un-revealed square.")
                    break
                else:
                    valid_input = ""
            if selection == "c":
                if base_grid[row_input][col_input] in ["_", "F"]:
                    print("Please select a revealed square.")
                    break
                else:
                    valid_input = ""
            if selection == "r":
                if base_grid[row_input][col_input] == "F":
                    print("Square already flagged. Unflag it to select it.")
                    break
                else:
                    valid_input = ""
        else:
            print(row_err + col_err)
    
    if valid_input == "":
        valid = 1

    return row_input, col_input, valid

def mark_square(user_row, user_col, base_grid, flags):
    """
    Docstring for mark_square
    
    :param row: Row selection
    :param col: Column selection

    This function marks a square which the user suspects is a bomb. This does two things: first, it lowers the count of "bombs remaining to mark" (not yet implemented) by 1, and it "locks" the square. The user will not be able to clear it without unmarking it. Neither "reveal" nor "clear region" should reveal a marked square.
    """
    if base_grid[user_row][user_col] == "_":
        base_grid[user_row][user_col] = "F"
        flags -= 1
    elif base_grid[user_row][user_col] == "F":
        base_grid[user_row][user_col] = "_"
        flags += 1
    return flags

def count_flags(row, col, base_grid):
    if row == 0 and col == 0:
        x = [base_grid[row][col+1], base_grid[row+1][col], base_grid[row+1][col+1]]
    elif row == 0 and col == len(base_grid[0])-1:
        x = [base_grid[row][col-1], base_grid[row+1][col-1], base_grid[row+1][col]]
    elif row == len(base_grid)-1 and col == 0:
        x = [base_grid[row-1][col], base_grid[row-1][col+1], base_grid[row][col+1]]
    elif row == len(base_grid)-1 and col == len(base_grid[0])-1:
        x = [base_grid[row-1][col-1], base_grid[row-1][col], base_grid[row-1][col-1]]
    elif row == 0 and col in range(1, len(base_grid[0])-1):
        x = [base_grid[row][col-1], 
             base_grid[row][col+1], 
             base_grid[row+1][col-1], 
             base_grid[row+1][col], 
             base_grid[row+1][col+1]]
    elif row in range(1, len(base_grid)-1) and col == 0:
        x = [base_grid[row-1][col], 
             base_grid[row-1][col+1], 
             base_grid[row][col+1], 
             base_grid[row+1][col], 
             base_grid[row+1][col+1]]
    elif row == len(base_grid)-1 and col in range(1, len(base_grid[0])-1):
        x = [base_grid[row-1][col-1], 
             base_grid[row-1][col], 
             base_grid[row-1][col+1], 
             base_grid[row][col-1], 
             base_grid[row][col+1]]
    elif row in range(1, len(base_grid)-1) and col == len(base_grid[0])-1:
        x = [base_grid[row-1][col-1], 
             base_grid[row-1][col], 
             base_grid[row][col-1], 
             base_grid[row+1][col-1], 
             base_grid[row+1][col]]
    else:
         x = [base_grid[row-1][col-1], 
              base_grid[row-1][col], 
              base_grid[row-1][col+1], 
              base_grid[row][col-1], 
              base_grid[row][col+1], 
              base_grid[row+1][col-1], 
              base_grid[row+1][col], 
              base_grid[row+1][col+1]]
    return x.count("F")

def clear_region(row, col, base_grid, dist_grid, status=1):
    width = len(base_grid[0])-1
    height = len(base_grid)-1
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    tmp = 1

    flags = count_flags(row, col, base_grid)
    expected_flags = 0 if base_grid[row][col] == " " else base_grid[row][col]

    if flags < expected_flags:
        print(f"Not enough flags. (found {flags}, expected {expected_flags})")
        return base_grid, status
    else:
        for dir in directions:
            new_row = row + dir[0]
            new_col = col + dir[1]

            if new_row < 0 or new_row > height or new_col < 0 or new_col > width:
                continue
            elif base_grid[new_row][new_col] != "F":
                base_grid, status = update_grid(base_grid, dist_grid, new_row, new_col)
                if status == 0:
                    tmp = 0
        if tmp == 0:
            status = 0
        return base_grid, status

"""    
def auto_clear(row, col, base_grid, dist_grid):
    width = len(base_grid[0])-1
    height = len(base_grid)-1
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    visited = [(row, col)]
    print(visited)

    # while True:
    for dir in directions:
        new_row = row + dir[0]
        new_col = col + dir[1]
        # print(dir)
        print((new_row, new_col) in visited)

        if (new_row, new_col) in visited:
            print(visited)
            continue
        else:
            visited.append((new_row, new_col))
        print(visited)

        if new_row < 0 or new_row > height or new_col < 0 or new_col > width:
            print("bingo")
            continue
        # elif is_corner(new_row, new_col, width, height) or is_edge(new_row, new_col, width, height):
        #     return auto_clear(base_grid, dist_grid, new_row, new_col)
        elif dist_grid[new_row][new_col] != " " and base_grid[new_row][new_col] != "F":
            print("bIIngo")
            return update_grid(base_grid, dist_grid, new_row, new_col)
            # base_grid[new_row][new_col] = dist_grid[new_row][new_col]
            continue
        elif base_grid[new_row][new_col] == "F":
            continue 
        else:
            print("bIIIngo!")
            return auto_clear(base_grid, dist_grid, new_row, new_col)
                # base_grid[new_row][new_col] = dist_grid[new_row][new_col]
                # if base_grid[new_row][new_col] != " ":
                #     continue
            # print(dir)
            # base_grid[new_row][new_col] == " "
        return
 """

def grid_count(base_grid):
    sum = 0
    for i in range(len(base_grid)):
        sum += base_grid[i].count("_")
        sum += base_grid[i].count("F")
    return sum

def check_flags(base_grid, dist_grid):
    for r in range(len(base_grid)):
        for c in range(len(base_grid[0])):
            if base_grid[r][c] == "F" and dist_grid[r][c] != "*":
                base_grid[r][c] = "x"
            if base_grid[r][c] == "_" and dist_grid[r][c] == "*":
                base_grid[r][c] = "*"
    return base_grid

def continue_game(new_game, status=1, moves=0, cleared=0, continue_game=1):
    cont = ""
    reset_game = ""
    while cont not in ["y", "n", "q"]:
        entry = input("Would you like to play again? [y/n] ").lower()
        try:
            cont = entry[0]
        except:
            continue
    if cont == "n":
        continue_game = 0
    elif cont == "q":
        sys.exit(1)
    else:
        while reset_game not in ["y", "n", "q"]:
            reset_entry = input("Reset board? [y/n] ").lower()
            try:
                reset_game = reset_entry[0]
            except:
                continue
        if reset_game == "q":
            sys.exit(1)
        if reset_game == "y":
            new_game = 1
        
    return status, moves, cleared, new_game, continue_game

def instructions():
    print("""Welcome to BOOMFINDER! Your goal is to reveal all of the 'safe' squares on the board, and avoid all of the BOOMs!

To set up the intial game board, select a width (3 - 10), a height (3 - 40), and number of bombs (minimum of 1, max of (width x height)-1). Leave any of these blank to use the default width and height, or to have BOOMFINDER calculate the optimal number of bombs for your grid.

1. Choose an action by typing the first letter (case insensetive) and pressing enter. You can take one of 3 actions: 
    1. You can REVEAL an unflagged square.
    2. You can CLEAR a region of squares.
    3. You can FLAG (or unFLAG) a square.
2. Next, choose a square by entering its coordinate in the form row, column where "row" and "column" are numbers.
3. The board will upated to display the result of the move, the number of flags you have remaining (which is also the number of BOOMs to find), the number of spaces you've cleared, and the number of spaces remaining to clear.
4. The game ends when you either clear all the spaces or reveal a BOOM

Notes:
On your first turn, you can only REVEAL or FLAG. On all other moves, CLEAR is available.

REVEAL: Reveal shows what is beneath the square - either blank, a number, or a BOOM. The number (or blank) indicates how many BOOMs are in the 8 squares surrounding it. '1' means that there is only 1 BOOM in the surrounding squares. 2 means there are 2, and 8 means that square is fully surrounded by BOOMs! Blank means that there are no bombs in any of the surrounding squares. You cannot reveal a flagged square. Revealing a square that has already been revealed has no effect.

If you find a BOOM, it's game over, so be careful!

FLAG: Flag allows you to mark a square that you suspect has a BOOM beneath it. If you've mistakenly flagged a square, simply use the FLAG move again to unflag the square.

CLEAR: Clear allows to to clear all unrevealed and unflagged squares surrounding a revealed square, but only if you have flagged the correct number of squares. For example, if you choose square (3,4) and the number revealed is '2', you must flag 2 of the surrounding squares before you can use CLEAR on (3,4). CLEAR will reveal all the unflagged squares, so if you flagged correctly, it's a quick way to reveal the board. If you haven't, you'll find a BOOM and the game will be over!

When the game ends, you have the option of continuing with the same setup, or resetting the board.

Enter 'q' at any time to quit the game.""")
    input("(press enter to continue)")

def title_print():
    t = random.randint(1, 17)
    
    match t:
        case 1:
            print(r"""
 ________  ________  ________  _____ ______   ________ ___  ________   ________  _______   ________     
|\   __  \|\   __  \|\   __  \|\   _ \  _   \|\  _____\\  \|\   ___  \|\   ___ \|\  ___ \ |\   __  \    
\ \  \|\ /\ \  \|\  \ \  \|\  \ \  \\\__\ \  \ \  \__/\ \  \ \  \\ \  \ \  \_|\ \ \   __/|\ \  \|\  \   
 \ \   __  \ \  \\\  \ \  \\\  \ \  \\|__| \  \ \   __\\ \  \ \  \\ \  \ \  \ \\ \ \  \_|/_\ \   _  _\  
  \ \  \|\  \ \  \\\  \ \  \\\  \ \  \    \ \  \ \  \_| \ \  \ \  \\ \  \ \  \_\\ \ \  \_|\ \ \  \\  \| 
   \ \_______\ \_______\ \_______\ \__\    \ \__\ \__\   \ \__\ \__\\ \__\ \_______\ \_______\ \__\\ _\ 
    \|_______|\|_______|\|_______|\|__|     \|__|\|__|    \|__|\|__| \|__|\|_______|\|_______|\|__|\|__|
""")
            return
        case 2:
            print(r""">>================================================================================<<
||                                                                                ||
||     dBBBBb   dBBBBP dBBBBP dBBBBBBb  dBBBBP dBP dBBBBb  dBBBBb  dBBBP dBBBBBb  ||
||        dBP  dB'.BP dB'.BP   '   dB'                dBP     dB'            dBP  ||
||    dBBBK'  dB'.BP dB'.BP dB'dB'dB' dBBBP  dBP dBP dBP dBP dB' dBBP    dBBBBK'  ||
||   dB' db  dB'.BP dB'.BP dB'dB'dB' dBP    dBP dBP dBP dBP dB' dBP     dBP  BB   ||
||  dBBBBP' dBBBBP dBBBBP dB'dB'dB' dBP    dBP dBP dBP dBBBBB' dBBBBP  dBP  dB'   ||
||                                                                                ||
>>================================================================================<<""")
            return
        case 3:
            print("\n")
            print(r"""▀█████████▄   ▄██████▄   ▄██████▄    ▄▄▄▄███▄▄▄▄      ▄████████  ▄█  ███▄▄▄▄   ████████▄     ▄████████    ▄████████
  ███    ███ ███    ███ ███    ███ ▄██▀▀▀███▀▀▀██▄   ███    ███ ███  ███▀▀▀██▄ ███   ▀███   ███    ███   ███    ███
  ███    ███ ███    ███ ███    ███ ███   ███   ███   ███    █▀  ███▌ ███   ███ ███    ███   ███    █▀    ███    ███
 ▄███▄▄▄██▀  ███    ███ ███    ███ ███   ███   ███  ▄███▄▄▄     ███▌ ███   ███ ███    ███  ▄███▄▄▄      ▄███▄▄▄▄██▀
▀▀███▀▀▀██▄  ███    ███ ███    ███ ███   ███   ███ ▀▀███▀▀▀     ███▌ ███   ███ ███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀▀▀  
  ███    ██▄ ███    ███ ███    ███ ███   ███   ███   ███        ███  ███   ███ ███    ███   ███    █▄  ▀███████████
  ███    ███ ███    ███ ███    ███ ███   ███   ███   ███        ███  ███   ███ ███   ▄███   ███    ███   ███    ███
▄█████████▀   ▀██████▀   ▀██████▀   ▀█   ███   █▀    ███        █▀    ▀█   █▀  ████████▀    ██████████   ███    ███
                                                                                                         ███    ███""")
            print("\n")
            return
        case 4:
            print("\n")
            print(r""" ███████████     ███████       ███████    ██████   ██████ ███████████ █████ ██████   █████ ██████████   ██████████ ███████████  
░░███░░░░░███  ███░░░░░███   ███░░░░░███ ░░██████ ██████ ░░███░░░░░░█░░███ ░░██████ ░░███ ░░███░░░░███ ░░███░░░░░█░░███░░░░░███ 
 ░███    ░███ ███     ░░███ ███     ░░███ ░███░█████░███  ░███   █ ░  ░███  ░███░███ ░███  ░███   ░░███ ░███  █ ░  ░███    ░███ 
 ░██████████ ░███      ░███░███      ░███ ░███░░███ ░███  ░███████    ░███  ░███░░███░███  ░███    ░███ ░██████    ░██████████  
 ░███░░░░░███░███      ░███░███      ░███ ░███ ░░░  ░███  ░███░░░█    ░███  ░███ ░░██████  ░███    ░███ ░███░░█    ░███░░░░░███ 
 ░███    ░███░░███     ███ ░░███     ███  ░███      ░███  ░███  ░     ░███  ░███  ░░█████  ░███    ███  ░███ ░   █ ░███    ░███ 
 ███████████  ░░░███████░   ░░░███████░   █████     █████ █████       █████ █████  ░░█████ ██████████   ██████████ █████   █████
░░░░░░░░░░░     ░░░░░░░       ░░░░░░░    ░░░░░     ░░░░░ ░░░░░       ░░░░░ ░░░░░    ░░░░░ ░░░░░░░░░░   ░░░░░░░░░░ ░░░░░   ░░░░░ """)
            print("\n")
            return
        case 5:
            print("\n")
            print(r"""______  _____  ________  _________ _____ _   _______ ___________ 
| ___ \|  _  ||  _  |  \/  ||  ___|_   _| \ | |  _  \  ___| ___ \
| |_/ /| | | || | | | .  . || |_    | | |  \| | | | | |__ | |_/ /
| ___ \| | | || | | | |\/| ||  _|   | | | . ` | | | |  __||    / 
| |_/ /\ \_/ /\ \_/ / |  | || |    _| |_| |\  | |/ /| |___| |\ \ 
\____/  \___/  \___/\_|  |_/\_|    \___/\_| \_/___/ \____/\_| \_|""")
            print("\n")
            return
        case 6:
            print("\n")
            print(r"""          )      )     *     (     (        )  (           (    
   (   ( /(   ( /(   (  `    )\ )  )\ )  ( /(  )\ )        )\ ) 
 ( )\  )\())  )\())  )\))(  (()/( (()/(  )\())(()/(   (   (()/( 
 )((_)((_)\  ((_)\  ((_)()\  /(_)) /(_))((_)\  /(_))  )\   /(_))
((_)_   ((_)   ((_) (_()((_)(_))_|(_))   _((_)(_))_  ((_) (_))  
 | _ ) / _ \  / _ \ |  \/  || |_  |_ _| | \| | |   \ | __|| _ \ 
 | _ \| (_) || (_) || |\/| || __|  | |  | .` | | |) || _| |   / 
 |___/ \___/  \___/ |_|  |_||_|   |___| |_|\_| |___/ |___||_|_\ """)
            print("\n")
            return
        case 7:
            print("\n")
            print(r""" __ )    _ \    _ \    \  |  ____| _ _|   \  |  __ \   ____|   _ \ 
 __ \   |   |  |   |  |\/ |  |       |     \ |  |   |  __|    |   |
 |   |  |   |  |   |  |   |  __|     |   |\  |  |   |  |      __ < 
____/  \___/  \___/  _|  _| _|     ___| _| \_| ____/  _____| _| \_\ """)
            print("\n")
            return
        case 8:
            print("\n")
            print(r"""██████╗  ██████╗  ██████╗ ███╗   ███╗███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝██║   ██║██║   ██║██╔████╔██║█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══██╗██║   ██║██║   ██║██║╚██╔╝██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                  """)
            print("\n")
            return
        case 9:
            print("\n")
            print(r"""BOOMFINDER
*   ** ** 
 ***  *  *
          
          
*         
          
   *   *  
      * * 
 ** *     
          
          
     *   *""")
            print("\n")
            return
        case 10:
            print("\n")
            print(r"""01000010 01001111 01001111 01001101 01000110 01001001 01001110 01000100 01000101 01010010 """)
            print("\n")
            return
        case 11:
            print("\n")
            print(r"""      ___           ___           ___           ___           ___                       ___           ___           ___           ___     
     /\  \         /\  \         /\  \         /\__\         /\  \          ___        /\__\         /\  \         /\  \         /\  \    
    /::\  \       /::\  \       /::\  \       /::|  |       /::\  \        /\  \      /::|  |       /::\  \       /::\  \       /::\  \   
   /:/\:\  \     /:/\:\  \     /:/\:\  \     /:|:|  |      /:/\:\  \       \:\  \    /:|:|  |      /:/\:\  \     /:/\:\  \     /:/\:\  \  
  /::\~\:\__\   /:/  \:\  \   /:/  \:\  \   /:/|:|__|__   /::\~\:\  \      /::\__\  /:/|:|  |__   /:/  \:\__\   /::\~\:\  \   /::\~\:\  \ 
 /:/\:\ \:|__| /:/__/ \:\__\ /:/__/ \:\__\ /:/ |::::\__\ /:/\:\ \:\__\  __/:/\/__/ /:/ |:| /\__\ /:/__/ \:|__| /:/\:\ \:\__\ /:/\:\ \:\__\
 \:\~\:\/:/  / \:\  \ /:/  / \:\  \ /:/  / \/__/~~/:/  / \/__\:\ \/__/ /\/:/  /    \/__|:|/:/  / \:\  \ /:/  / \:\~\:\ \/__/ \/_|::\/:/  /
  \:\ \::/  /   \:\  /:/  /   \:\  /:/  /        /:/  /       \:\__\   \::/__/         |:/:/  /   \:\  /:/  /   \:\ \:\__\      |:|::/  / 
   \:\/:/  /     \:\/:/  /     \:\/:/  /        /:/  /         \/__/    \:\__\         |::/  /     \:\/:/  /     \:\ \/__/      |:|\/__/  
    \::/__/       \::/  /       \::/  /        /:/  /                    \/__/         /:/  /       \::/__/       \:\__\        |:|  |    
     ~~            \/__/         \/__/         \/__/                                   \/__/         ~~            \/__/         \|__|    """)
            print("\n")
            return
        case 12:
            print("\n")
            print(r"""                    ___           ___           ___           ___                       ___                         ___           ___     
     _____         /\  \         /\  \         /\  \         /\__\                     /\  \         _____         /\__\         /\  \    
    /::\  \       /::\  \       /::\  \       |::\  \       /:/ _/_       ___          \:\  \       /::\  \       /:/ _/_       /::\  \   
   /:/\:\  \     /:/\:\  \     /:/\:\  \      |:|:\  \     /:/ /\__\     /\__\          \:\  \     /:/\:\  \     /:/ /\__\     /:/\:\__\  
  /:/ /::\__\   /:/  \:\  \   /:/  \:\  \   __|:|\:\  \   /:/ /:/  /    /:/__/      _____\:\  \   /:/  \:\__\   /:/ /:/ _/_   /:/ /:/  /  
 /:/_/:/\:|__| /:/__/ \:\__\ /:/__/ \:\__\ /::::|_\:\__\ /:/_/:/  /    /::\  \     /::::::::\__\ /:/__/ \:|__| /:/_/:/ /\__\ /:/_/:/__/___
 \:\/:/ /:/  / \:\  \ /:/  / \:\  \ /:/  / \:\~~\  \/__/ \:\/:/  /     \/\:\  \__  \:\~~\~~\/__/ \:\  \ /:/  / \:\/:/ /:/  / \:\/:::::/  /
  \::/_/:/  /   \:\  /:/  /   \:\  /:/  /   \:\  \        \::/__/       ~~\:\/\__\  \:\  \        \:\  /:/  /   \::/_/:/  /   \::/~~/~~~~ 
   \:\/:/  /     \:\/:/  /     \:\/:/  /     \:\  \        \:\  \          \::/  /   \:\  \        \:\/:/  /     \:\/:/  /     \:\~~\     
    \::/  /       \::/  /       \::/  /       \:\__\        \:\__\         /:/  /     \:\__\        \::/  /       \::/  /       \:\__\    
     \/__/         \/__/         \/__/         \/__/         \/__/         \/__/       \/__/         \/__/         \/__/         \/__/    """)
            print("\n")
            return
        case 13:
            print("\n")
            print(r"""                    ___           ___           ___           ___                     ___          _____          ___           ___     
     _____         /  /\         /  /\         /__/\         /  /\      ___          /__/\        /  /::\        /  /\         /  /\    
    /  /::\       /  /::\       /  /::\       |  |::\       /  /:/_    /  /\         \  \:\      /  /:/\:\      /  /:/_       /  /::\   
   /  /:/\:\     /  /:/\:\     /  /:/\:\      |  |:|:\     /  /:/ /\  /  /:/          \  \:\    /  /:/  \:\    /  /:/ /\     /  /:/\:\  
  /  /:/~/::\   /  /:/  \:\   /  /:/  \:\   __|__|:|\:\   /  /:/ /:/ /__/::\      _____\__\:\  /__/:/ \__\:|  /  /:/ /:/_   /  /:/~/:/  
 /__/:/ /:/\:| /__/:/ \__\:\ /__/:/ \__\:\ /__/::::| \:\ /__/:/ /:/  \__\/\:\__  /__/::::::::\ \  \:\ /  /:/ /__/:/ /:/ /\ /__/:/ /:/___
 \  \:\/:/~/:/ \  \:\ /  /:/ \  \:\ /  /:/ \  \:\~~\__\/ \  \:\/:/      \  \:\/\ \  \:\~~\~~\/  \  \:\  /:/  \  \:\/:/ /:/ \  \:\/:::::/
  \  \::/ /:/   \  \:\  /:/   \  \:\  /:/   \  \:\        \  \::/        \__\::/  \  \:\  ~~~    \  \:\/:/    \  \::/ /:/   \  \::/~~~~ 
   \  \:\/:/     \  \:\/:/     \  \:\/:/     \  \:\        \  \:\        /__/:/    \  \:\         \  \::/      \  \:\/:/     \  \:\     
    \  \::/       \  \::/       \  \::/       \  \:\        \  \:\       \__\/      \  \:\         \__\/        \  \::/       \  \:\    
     \__\/         \__\/         \__\/         \__\/         \__\/                   \__\/                       \__\/         \__\/    """)
            print("\n")
            return
        case 14:
            print("\n")
            print(r"""      ___           ___           ___           ___                                      ___           ___           ___           ___     
     /  /\         /  /\         /  /\         /  /\          ___            ___        /  /\         /  /\         /  /\         /  /\    
    /  /::\       /  /::\       /  /::\       /  /::|        /  /\          /__/\      /  /::|       /  /::\       /  /::\       /  /::\   
   /  /:/\:\     /  /:/\:\     /  /:/\:\     /  /:|:|       /  /::\         \__\:\    /  /:|:|      /  /:/\:\     /  /:/\:\     /  /:/\:\  
  /  /::\ \:\   /  /:/  \:\   /  /:/  \:\   /  /:/|:|__    /  /:/\:\        /  /::\  /  /:/|:|__   /  /:/  \:\   /  /::\ \:\   /  /::\ \:\ 
 /__/:/\:\_\:| /__/:/ \__\:\ /__/:/ \__\:\ /__/:/_|::::\  /  /::\ \:\    __/  /:/\/ /__/:/ |:| /\ /__/:/ \__\:| /__/:/\:\ \:\ /__/:/\:\_\:\
 \  \:\ \:\/:/ \  \:\ /  /:/ \  \:\ /  /:/ \__\/  /~~/:/ /__/:/\:\ \:\  /__/\/:/~~  \__\/  |:|/:/ \  \:\ /  /:/ \  \:\ \:\_\/ \__\/~|::\/:/
  \  \:\_\::/   \  \:\  /:/   \  \:\  /:/        /  /:/  \__\/  \:\_\/  \  \::/         |  |:/:/   \  \:\  /:/   \  \:\ \:\      |  |:|::/ 
   \  \:\/:/     \  \:\/:/     \  \:\/:/        /  /:/        \  \:\     \  \:\         |__|::/     \  \:\/:/     \  \:\_\/      |  |:|\/  
    \__\::/       \  \::/       \  \::/        /__/:/          \__\/      \__\/         /__/:/       \__\::/       \  \:\        |__|:|~   
        ~~         \__\/         \__\/         \__\/                                    \__\/            ~~         \__\/         \__\|    """)
            print("\n")
            return
        case 15:
            print("\n")
            print(r"""┳┓┏┓┏┓┳┳┓┏┓┳┳┓┳┓┏┓┳┓
┣┫┃┃┃┃┃┃┃┣ ┃┃┃┃┃┣ ┣┫
┻┛┗┛┗┛┛ ┗┻ ┻┛┗┻┛┗┛┛┗
                    """)
            return
        case 16:
            print("\n")
            print(r"""__/\\\\\\\\\\\\\_________/\\\\\____________/\\\\\_______/\\\\____________/\\\\__/\\\\\\\\\\\\\\\__/\\\\\\\\\\\__/\\\\\_____/\\\__/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\____/\\\\\\\\\_____        
 _\/\\\/////////\\\_____/\\\///\\\________/\\\///\\\____\/\\\\\\________/\\\\\\_\/\\\///////////__\/////\\\///__\/\\\\\\___\/\\\_\/\\\////////\\\__\/\\\///////////___/\\\///////\\\___       
  _\/\\\_______\/\\\___/\\\/__\///\\\____/\\\/__\///\\\__\/\\\//\\\____/\\\//\\\_\/\\\_________________\/\\\_____\/\\\/\\\__\/\\\_\/\\\______\//\\\_\/\\\_____________\/\\\_____\/\\\___      
   _\/\\\\\\\\\\\\\\___/\\\______\//\\\__/\\\______\//\\\_\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\_________\/\\\_____\/\\\//\\\_\/\\\_\/\\\_______\/\\\_\/\\\\\\\\\\\_____\/\\\\\\\\\\\/____     
    _\/\\\/////////\\\_\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\__\///\\\/___\/\\\_\/\\\///////__________\/\\\_____\/\\\\//\\\\/\\\_\/\\\_______\/\\\_\/\\\///////______\/\\\//////\\\____    
     _\/\\\_______\/\\\_\//\\\______/\\\__\//\\\______/\\\__\/\\\____\///_____\/\\\_\/\\\_________________\/\\\_____\/\\\_\//\\\/\\\_\/\\\_______\/\\\_\/\\\_____________\/\\\____\//\\\___   
      _\/\\\_______\/\\\__\///\\\__/\\\_____\///\\\__/\\\____\/\\\_____________\/\\\_\/\\\_________________\/\\\_____\/\\\__\//\\\\\\_\/\\\_______/\\\__\/\\\_____________\/\\\_____\//\\\__  
       _\/\\\\\\\\\\\\\/_____\///\\\\\/________\///\\\\\/_____\/\\\_____________\/\\\_\/\\\______________/\\\\\\\\\\\_\/\\\___\//\\\\\_\/\\\\\\\\\\\\/___\/\\\\\\\\\\\\\\\_\/\\\______\//\\\_ 
        _\/////////////_________\/////____________\/////_______\///______________\///__\///______________\///////////__\///_____\/////__\////////////_____\///////////////__\///________\///__""")
            print("\n")
            return
        case 17:
            print("\n")
            print(r"""░       ░░░░      ░░░░      ░░░  ░░░░  ░░        ░░        ░░   ░░░  ░░       ░░░        ░░       ░░
▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒   ▒▒   ▒▒  ▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒    ▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒
▓       ▓▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓        ▓▓      ▓▓▓▓▓▓▓  ▓▓▓▓▓  ▓  ▓  ▓▓  ▓▓▓▓  ▓▓      ▓▓▓▓       ▓▓
█  ████  ██  ████  ██  ████  ██  █  █  ██  ███████████  █████  ██    ██  ████  ██  ████████  ███  ██
█       ████      ████      ███  ████  ██  ████████        ██  ███   ██       ███        ██  ████  █
                                                                                                    """)
            print("\n")
            return
        case _:
            return
        
def main():
    board_width, board_height, number_of_bombs = 5, 5, 3
    base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
    bomb_grid = bomb_placement(board_width, board_height, number_of_bombs, 1, 1)
    dist_grid = calc_dist(board_width, board_height, bomb_grid)

main()