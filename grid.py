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
    for row in range(len(bomb_grid)):
        for col in range(len(bomb_grid[row])):
            # print(f"{row=}, {col=}")
            if bomb_grid[row][col] == 1:
                dist_grid[row][col] += 9
            elif row == 0:
                if col == 0:
                    dist_grid[row][col] += (bomb_grid[row][col+1] + bomb_grid[row+1][col] + bomb_grid[row+1][col+1])
                elif col == width - 1:
                    dist_grid[row][col] += (bomb_grid[row][col-1] + bomb_grid[row+1][col-1] + bomb_grid[row+1][col])
                else:
                    dist_grid[row][col] += (bomb_grid[row][col-1] + bomb_grid[row][col+1] + bomb_grid[row+1][col-1] + bomb_grid[row+1][col] + bomb_grid[row+1][col+1])
            elif row == height - 1:
                if col == 0:
                    dist_grid[row][col] += (bomb_grid[row-1][col] + bomb_grid[row-1][col+1] + bomb_grid[row][col+1])
                elif col == width - 1:
                    dist_grid[row][col] += (bomb_grid[row-1][col-1] + bomb_grid[row-1][col] + bomb_grid[row][col-1])
                else:
                    dist_grid[row][col] += (bomb_grid[row-1][col-1] + bomb_grid[row-1][col] + bomb_grid[row-1][col+1] + bomb_grid[row][col-1] + bomb_grid[row][col+1])
            elif col == 0:
                dist_grid[row][col] += (bomb_grid[row-1][col] + bomb_grid[row-1][col+1] + bomb_grid[row][col+1] + bomb_grid[row+1][col] + bomb_grid[row+1][col+1])
            elif col == width - 1:
                dist_grid[row][col] += (bomb_grid[row-1][col-1] + bomb_grid[row-1][col] + bomb_grid[row][col-1] + bomb_grid[row+1][col-1] + bomb_grid[row+1][col])
            else:
                dist_grid[row][col] += (bomb_grid[row-1][col-1] + bomb_grid[row-1][col] + bomb_grid[row-1][col+1] + bomb_grid[row][col-1] + bomb_grid[row][col+1] + bomb_grid[row+1][col-1] + bomb_grid[row+1][col] + bomb_grid[row+1][col+1])
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

    width_entry = input("Set the board width: ")
    if not width_entry.isnumeric():
        print("Invalid entry, using default")
    elif int(width_entry) < 3:
        print("Board too small, defaulting to 3")
        board_width = 3
    elif int(width_entry) > constants.MAX_BOARD_WIDTH:
        print(f"Board too wide, limiting to {constants.MAX_BOARD_WIDTH}.")
        board_width = constants.MAX_BOARD_WIDTH
    else:
        board_width = int(width_entry)  
      
    height_entry = input("Set the board height: ")
    if not height_entry.isnumeric():
        print("Invalid entry, using default")
    elif int(height_entry) < 3:
        print("Board too small, defaulting to 3.")
        board_height = 3
    elif int(height_entry) > constants.MAX_BOARD_HEIGHT:
        print(f"Board too tall. Limiting to {constants.MAX_BOARD_HEIGHT}.")
        board_height = constants.MAX_BOARD_HEIGHT
    else:
        board_height = int(height_entry)

    bombs_entry = input("How many BOOMS? ")
    if not bombs_entry.isnumeric():
        print("BOOMS calculated automatically")
        bombs_raw = (0.00708274 * (board_width * board_height)**1.53966) + 3.85371
        number_of_bombs = int(bombs_raw)
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
