import sys
import grid

def move_selection(base_grid):
    """
    Docstring for move_selection
    
    :param choice: What type of move player would like to take. Can be to reveal a square, flag/mark a square (or unmark it), or clear a region around a square

    revealing a square is already implemented elsewhere, just needs to be moved into functions.

    flagging a square will involve putting a mark on a suspected bomb, and will "lock" that square - it will not be selectable by the user, and won't reveal if user clears the region (or if it was blank and consecutive blank squares are cleared (this functionality is not yet implemented)). If chosen as first move, will not set the bombs placement, but the flags should not influence bomb placement (meaning if the user wants to place all the flags before revealing any squares, there is a tiny-but-not-zero chance all the bombs will be placed under marked squares).

    clearing a region clears the (up to) 8 squares (three on corners, 5 on edges) around the selection. ONLY already cleared squares can be selected, unlike revealing a square. Consecutive empty squares should clear. Any bombs in the surrounding squares trigger a game over. Cannot be chosen as the first move.
    """
    selection = None
    print("What type of move would you like to make?")
    while selection not in ["r", "c", "f"]:
        selection = input("Reveal (r), Clear (c), Flag/Unflag (f): ").lower()
    match selection:
        case "r":
            pass
        case "c":
            pass
        case "f":
            base_grid = grid.mark_square(base_grid)
            
        case _:
            print("Look...")

def other_move(board_width, board_height, base_grid, dist_grid, status, moves):
    """
    Docstring for other_move
    
    :param row: Row selection
    :param col: Column selection

    This function handles any selection to reveal a square after the first move. Bombs have been placed.

    As with all moves, this function needs to ensure the move is valid - numeric, within the constraints of the board, unmarked, and whether the square has already been revealed. If any of these checks fail, it should ask for another selection (though, I suppose in the case of an already-revealed square, it could just operate the same, returning the same board - i.e. nothing happens).

    This move also must check if the square is a bomb. If so, the game ends.

    If it is not a bomb, it reveals the number of bombs in the adjacent squares. If the distance is zero, the square is blank. Any other blank squares touching this one should also be revealed.

    It is possible that clearing all consecutive blank squares could reveal all safe squares (usually for bigger grids with fewer bombs), so the function needs to check if the user has won.

    The function must also check whether the revealed square itself is the last safe square, which would result in the user winning.
    """
    valid_move = "continue"
    while valid_move not in ["valid", "clear"]:
        # print(valid_move)
        if valid_move == "flagged":
            print("Square already flagged. Unflag it to select it.")
            cleared = (board_width * board_height) - grid.grid_count(base_grid)
            return base_grid, status, cleared, moves
        user_input = input("Select a square: ")
        if user_input == "q":
            sys.exit(1)
        row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
        valid_move = grid.validate_input(row_input, col_input, "other_move", base_grid)
    player_row, player_col = int(row_input)-1, int(col_input)-1
    if "move_type" == "c":
        base_grid, status = grid.clear_region(player_row, player_col, base_grid, dist_grid)
        print(f"{status=}")
        moves += 1
    else:
        base_grid, status = grid.update_grid(base_grid, dist_grid, player_row, player_col)
    moves += 1
    cleared = (board_width * board_height) - grid.grid_count(base_grid)
    return base_grid, status, cleared, moves

def validate_input(row, col, type, base_grid):
    """
    Docstring for validate_input
    
    :param row: Row selection
    :param col: Column selection
    :param type: What type of move was selected

    For all move types, function needs to validate the input is within the game board.

    For revealing a square, function needs to validate the selection is not flagged.

    For clearing a region, function needs to validate the selection HAS been selected before and is not flagged.

    For marking a square, function needs to validate there are flags remaining, and that the selection has not been revealed already.
    """
    res = ""
    if type == "first_move":
        if not row.isnumeric() or int(row)-1 not in range(0, len(base_grid)):
            res += f"Row must be a number between 1 and {len(base_grid)}. "
        if not col.isnumeric() or int(col)-1 not in range(0, len(base_grid[0])):
            res += f"Column must be a number between 1 and {len(base_grid[0])}."
        return res
    
    if type == "other_move":
        err = 0
        if not row.isnumeric() or int(row)-1 not in range(0, len(base_grid)):
            res += f"Row must be a number between 1 and {len(base_grid)}. "
            err += 1
        if not col.isnumeric() or int(col)-1 not in range(0, len(base_grid[0])):
            res += f"Column must be a number between 1 and {len(base_grid[0])}."
            err += 1
        
        if err != 0:
            return res

        row = int(row) - 1
        col = int(col) - 1
        if base_grid[row][col] == "F":
            res = "flagged"
        elif base_grid[row][col] != "_":  # This will go away later
            res = "clear"
        else:
            res = "valid"
        return res
    
    if type == "mark":
        err = 0
        if not row.isnumeric() or int(row)-1 not in range(0, len(base_grid)):
            res += f"Row must be a number between 1 and {len(base_grid)}. "
            err += 1
        if not col.isnumeric() or int(col)-1 not in range(0, len(base_grid[0])):
            res += f"Column must be a number between 1 and {len(base_grid[0])}."
            err += 1
        
        if err != 0:
            return res
        
        row = int(row) - 1
        col = int(col) - 1

        if base_grid[row][col] != "_" and base_grid[row][col] != "F":
            res = "Please select a square that has not been revealed."
        
        return res

def clear_region_old(row, col, base_grid, dist_grid):
    """
    Docstring for clear_region
    
    :param row: Row selection
    :param col: Column selection

    This function reveals any adjacent unflagged  squares around the selection. Square must have been revealed. Revealed squares behave exactly as in other_move() - if there is no bomb, the distance is revealed; if it is blank, the consectutive blank squares are revealed; if there is a bomb, the game ends.

    Function will need to check that the selected square HAS been previously selected or if it is flagged (for messaging purposes). If this check passes, function will call a modified version of other_move(), in that the game won't ask for another input if the square has already been cleared or is flagged, it just ignores it.

    Will also need to check that the correct number of squares have been flagged.

    This option should only appear after the first move.
    """
    height = len(base_grid)-1
    width = len(base_grid[0])-1
    row_range = range(-1, 2)
    col_range = range(-1, 2)
    status = 1
    tmp = 1

    flags = grid.count_flags(row, col, base_grid)
    expected_flags = 0 if base_grid[row][col] == " " else base_grid[row][col]

    if flags != expected_flags:
        print(f"Not enough flags. (found {flags}, expected {expected_flags})")
        return base_grid, status
    
    row_range, col_range = ranges(row, col, width, height)

    if is_corner(row, col, height, width):
        if row == 0 and col == 0:
            row_range = range(0, 2)
            col_range = range(0, 2)
        if row == 0 and col == width:
            row_range = range(0, 2)
            col_range = range(-1,1)
        if row == height and col == 0:
            row_range = range(-1,1)
            col_range = range(0, 2)
        if row == height and col == width:
            row_range = range(-1, 1)
            col_range = range(-1, 1)
    
    if is_edge(row, col, height, width):
        if row == 0:
            row_range = range(0, 2)
        if row == height:
            row_range = range(-1, 1)
        if col == 0:
            col_range = range(0, 2)
        if col == width:
            col_range = range(-1, 1)
    # print(f"{width=}")
    # print(f"{height=}")
    for r in row_range:
        for c in col_range:
            # print(f"{row=}, {r=}, {row+r}, {col=}, {c=}, {col+c}")
            if r == 0 and c == 0:
                continue
            base_grid, status = grid.update_grid(base_grid, dist_grid, row+r, col+c)
            if status == 0:
                tmp = 0
    if tmp == 0:
        status = 0
    return base_grid, status

def ranges(row, col, width, height):
    row_range = range(-1, 2)
    col_range = range(-1, 2)
    if row == 0 and col == 0:
        row_range = range(0, 2)
        col_range = range(0, 2)
    elif row == 0 and col == width:
        row_range = range(0, 2)
        col_range = range(-1,1)
    elif row == height and col == 0:
        row_range = range(-1,1)
        col_range = range(0, 2)
    elif row == height and col == width:
        row_range = range(-1, 1)
        col_range = range(-1, 1)
    elif row == 0:
        row_range = range(0, 2)
    elif row == height:
        row_range = range(-1, 1)
    elif col == 0:
        col_range = range(0, 2)
    elif col == width:
        col_range = range(-1, 1)
    return row_range, col_range

def is_corner(row, col, width, height):
    if row == 0 and col == 0:
        return True
    if row == 0 and col == width:
        return True
    if row == height and col == 0:
        return True
    if row == height and col == width:
        return True
    return False

def is_edge(row, col, width, height):
    if not is_corner(row, col, width, height):
        if row == 0 or row == height or col == 0 or col == width:
            return True
    return False

def auto_clear_dep(row, col, base_grid, dist_grid):
    """
    Docstring for auto_clear
    
    :param row: Row selection
    :param col: Column selection
    :param base_grid: The game board to be displayed to player
    :param dist_grid: The underlying grid that lists the number of bombs adjacent to current square

    I think this might be a recursive function. It would be called if the number of bombs around a revealed square is zero. It checks each adjacent square. If the adjacent square is zero, it checks each square adjacent to it.

    Function accpets the current row and column. 
    
    We know dist_grid[row][col] == 0, so we know that the surrounding squares can be revealed. I don't think it matters where this starts, but keeping it consistent will be important. I think we could start by revealing all of the squares, and then checking if any are 0; or we could start by revealing one square, and then checking if it is zero and calling this function again, until we get to a square that isn't zero and stepping back.

    We would then call update_grid(row-1, col-1)

    I am TERRIBLE at recursion. Ugh.
    """
    width = len(base_grid[0])-1
    height = len(base_grid)-1
    row_range, col_range = ranges(row, col, width, height)

    if row == 0 or dist_grid[row][col] != " ":
        return base_grid
    else: 
        grid.update_grid(base_grid, dist_grid, row-1, col)
    if row == height or dist_grid[row][col] != " ":
        return base_grid
    else:
        grid.update_grid(base_grid, dist_grid, row+1, col)
    if col == 0 or dist_grid[row][col] != " ":
        return base_grid
    else:
        grid.update_grid(base_grid, dist_grid, row, col-1)
    if col == width or dist_grid[row][col] != " ":
        return base_grid
    else:
        grid.update_grid(base_grid, dist_grid, row, col+1)
    # else:
        # print(f"{row_range=}, {col_range=}")
        # for r in row_range:
        #     for c in col_range:
        #         update_grid(base_grid, dist_grid, row+r, col+c)
        # update_grid(base_grid, dist_grid, row-1, col)
    """ row_range, col_range = ranges(row, col, width, height)
    for r in row_range:
        for c in col_range:
            if r == 0 and c == 0:
                continue
            if dist_grid[row+r][col+c] != " ":
                base_grid[row+r][col+c] = dist_grid[row+r][col+c]
                break
            else:
                update_grid(base_grid, dist_grid, row+r, col+c)
                # base_grid[row+r][col+c] = dist_grid[row+r][col+c]
                # auto_clear(base_grid, dist_grid, row+r, col+c) """


def first_move(player_row, player_col, board_width, board_height, number_of_bombs, base_grid, status=1, moves=0):
    """
    Docstring for first_move
    
    :param row: Row selection
    :param col: Column selection

    This is the function for the first square reveal of the game. This is a unique move because the bombs are not placed until the user selects a square to reveal. This is mainly to guarantee the game actually starts, but also becuase that's how I've always assumed the Windows game did it.

    As with all moves, this function needs to ensure the move is valid - numeric, within the constraints of the board, and unmarked. If any of these checks fail, it should ask for another selection.

    As this is the first move, checking for a bomb is uneccesary. The function must, however call bomb_placement(), and then updated the game board with the number of bombs in adjacent squares, if any.

    If the number is zero, the square is blank. Any other blank squares touching this one should also be revealed. 

    It is possible that clearing all consecutive blank squares could reveal all safe squares (usually for bigger grids with fewer bombs), so the function needs to check if the user has won.
    """
    # user_input = input("Select a square: ")
    # row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
    # valid_move = validate_input(row_input, col_input, "first_move", base_grid)
    # valid_move = "start"
    # while valid_move != "":
    #     # print(valid_move)
    #     user_input = input("Select a square: ")
    #     if user_input == "q":
    #         sys.exit(1)
    #     row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
    #     valid_move = validate_input(row_input, col_input, "first_move", base_grid)
    #     flag_check = validate_input(row_input, col_input, "other_move", base_grid)
    #     if flag_check == "flagged":
    #         print("Square already flagged. Unflag it to select it.")
    #         return base_grid, status, None, 0, 0
    # player_row, player_col = int(row_input)-1, int(col_input)-1
    bomb_grid = grid.bomb_placement(board_width, board_height, number_of_bombs, player_row, player_col)
    dist_grid = grid.calc_dist(board_width, board_height, bomb_grid)
    # print_grid(dist_grid)
    base_grid, status = grid.update_grid(base_grid, dist_grid, player_row, player_col)
    moves += 1
    cleared = (board_width * board_height) - grid.grid_count(base_grid)
    return base_grid, status, dist_grid, moves, cleared


def mark_square(user_row, user_col, base_grid, flags):
    """
    Docstring for mark_square
    
    :param row: Row selection
    :param col: Column selection

    This function marks a square which the user suspects is a bomb. This does two things: first, it lowers the count of "bombs remaining to mark" (not yet implemented) by 1, and it "locks" the square. The user will not be able to clear it without unmarking it. Neither "reveal" nor "clear region" should reveal a marked square.

    This function will need to check that the square is within the board, has not already been revealed, whehter it is flagged or not, and how many flags the user has remaining (though the classic game allows player to place as many as they'd like).

    If the selection has been marked, the marked should be removed and remaining flags increased by 1.

    Using all flags does not trigger an end game check. It just means a user can't place any more flags until they unmark a square. If all squares are marked, this option will only unmark a square.
    """
    # validate_input = "start"
    # user_input = input("Select a square: ")
    # row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
    # valid_input = validate_input(row_input, col_input, "mark", base_grid)
    # while valid_input != "":
    #     print(valid_input)
    #     user_input = input("Select a square: ")
    #     row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
    #     valid_input = validate_input(row_input, col_input, "mark", base_grid)

    # user_row, user_col = int(row_input)-1, int(col_input)-1
    if base_grid[user_row][user_col] == "_":
        base_grid[user_row][user_col] = "F"
        flags -= 1
    elif base_grid[user_row][user_col] == "F":
        base_grid[user_row][user_col] = "_"
        flags += 1
    return flags

def main():
    # defaults
    board_width = 6
    board_height = 6
    bombs_raw = (0.00708274 * (board_width * board_height)**1.53966) + 3.85371
    number_of_bombs = int(bombs_raw)
    number_of_safes = board_width * board_height - number_of_bombs
    
    """ print("Let's Find Some BOOMS!")
    width_entry = input("Set the board width: ")
    if not width_entry.isnumeric():
        print(f"Invalid entry, using default ({board_height})")
    else:
        board_width = int(width_entry)    
    height_entry = input("Set the board height: ")
    if not height_entry.isnumeric():
        print(f"Invalid entry, using default ({board_width})")
    else:
        board_height = int(height_entry)
    bombs_entry = input("How many BOOMS? ")
    if not bombs_entry.isnumeric():
        print("BOOMS calculated automatically")
        bombs_raw = (0.00708274 * (board_width * board_height)**1.53966) + 3.85371
        number_of_bombs = int(bombs_raw)
    else:
        number_of_bombs = int(bombs_entry) """

    board_width, board_height, number_of_bombs, number_of_safes = grid.intialize_grid(board_width, board_height)
    print(f"BOOMS to avoid: {number_of_bombs}")
    # number_of_safes = board_width * board_height - number_of_bombs

    base_grid = [['_' for x in range(board_width)] for y in range(board_height)]

    # moves = [] # list of player moves
    # print_grid(base_grid)
    status = 1
    continue_game = 1
    moves = 0
    cleared = 0
    flags = number_of_bombs

    while continue_game == 1:
        # if status == 1:
        grid.print_grid(base_grid)
        print(f"{cleared=}")
        print(f"Flags remaining: {flags}")

        # move_selection(base_grid)
        # print_grid(base_grid)
        # print(f"{status=}")
        selection = None
        print("What type of move would you like to make?")
        while selection not in ["r", "c", "f"]:
            selection = input("Reveal (r), Clear (c), Flag/Unflag (f): ").lower()
        if selection == "f":
            flags = mark_square(base_grid, flags)
            # print_grid(base_grid)
        
        # if selection == "c" and moves > 0:
        #     user_input = input("Select a square: ")
        #     row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
        #     while valid_move != "":
        #         print(valid_move)
        #         user_input = input("Select a square: ")
        #         row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
        #         valid_move = validate_input(row_input, col_input, "other_move", base_grid)
        #     player_row, player_col = int(row_input)-1, int(col_input)-1
        #     clear_region_2(player_row, player_col, base_grid, dist_grid)
        #     cleared = (board_width * board_height) - grid_count(base_grid)
        
        if selection == "r" or selection == "c":
            # print(f"{moves=}")
            # user_input = input("Select a square: ")
            # row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]

            # if len(moves) < 1:
            if moves == 0:
                base_grid, status, bomb_grid, dist_grid, moves, cleared = first_move(board_width, board_height, number_of_bombs, base_grid)
                # valid_move = validate_input(row_input, col_input, "first_move", base_grid)

                # while valid_move != "":
                #     print(valid_move)
                #     user_input = input("Select a square: ")
                #     row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
                #     valid_move = validate_input(row_input, col_input, "first_move", base_grid)
                # player_row, player_col = int(row_input)-1, int(col_input)-1
                # move = (player_row, player_col)
                # bomb_grid = bomb_placement(board_width, board_height, number_of_bombs, player_row, player_col)
                # print_grid(bomb_grid)
                # dist_grid = calc_dist(board_width, board_height, bomb_grid)
                # print_grid(dist_grid)
                # moves.append(move)
                # base_grid, status = update_grid(base_grid, dist_grid, player_row, player_col)
                # moves += 1
                # cleared = (board_width * board_height) - grid_count(base_grid)
                # all_cleared_check()
            else:
                pass
                # base_grid, status, cleared, moves = other_move(board_width, board_height, base_grid, dist_grid, status, moves)
                # valid_move = validate_input(row_input, col_input, "other_move", base_grid)
                # while valid_move not in ["valid", "clear", "flagged"]:
                #     print(valid_move)
                #     user_input = input("Select a square: ")
                #     row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
                #     valid_move = validate_input(row_input, col_input, "other_move", base_grid)
                    
                # player_row, player_col = int(row_input)-1, int(col_input)-1

                # if valid_move == "clear":
                #     base_grid, status = clear_region(player_row, player_col, base_grid, dist_grid)
                #     print(f"{status=}")
                #     moves += 1
                # elif valid_move == "flagged":
                #     print(f"({row_input}, {col_input}) is flagged, select again.")
                # elif valid_move == "valid":
                #     # move = {player_row, player_col}
                #     # moves.append(move)
                #     base_grid, status = update_grid(base_grid, dist_grid, player_row, player_col)
                #     moves += 1
                # cleared = (board_width * board_height) - grid_count(base_grid)
                # if cleared == number_of_safes:
                #     base_grid, status = check_flags(base_grid, bomb_grid)
            
            if cleared == number_of_safes and status == 1:
                # base_grid, status = check_flags(base_grid, bomb_grid)
                grid.print_grid(base_grid)
                print("All spaces cleared! You win!")
                cont = input("Would you like to play again? ").lower()
                if cont == "n" or cont == "no":
                    continue_game = 0
                else:
                    moves = 0
                    cleared = 0
                    flags = number_of_bombs
                    # status = 1
                    base_grid = [['_' for x in range(board_width)] for y in range(board_height)]

            # elif status == 2:
            #     # if cleared == number_of_safes:
            #     print_grid(base_grid)
            #     print("All spaces cleared! You win!")
            #     cont = input("Would you like to play again? ").lower()
            #     if cont == "n" or cont == "no":
            #         continue_game = 0
            #     else:
            #         moves = 0
            #         cleared = 0
            #         status = 1
            #         base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
            #         # print_grid(base_grid)
            
            if status == 0:
                    cleared = 0
                    # print_grid(base_grid)
                    cont = input("Would you like to play again? ").lower()
                    if cont == "n" or cont == "no":
                        continue_game = 0
                    else:
                        status = 1
                        moves = 0
                        flags = number_of_bombs
                        # cleared = 0
                        base_grid = [['_' for x in range(board_width)] for y in range(board_height)]

        
                # print_grid(base_grid)    
    """      

        while move in moves:
            print("Square already selected. Please select again.")
            player_row = int(input("Select a row: "))-1
            player_col = int(input("Select a column: "))-1
            # clear_region(player_row, player_col, base_grid, dist_grid)
            move = (player_row, player_col)
        
        
        


        if status == 1:
            if len(moves) == number_of_safes:
                print("All spaces cleared! You win!")
                cont = input("Would you like to play again? ").lower()
                if cont == "n" or cont == "no":
                    continue_game = 0
                else:
                    moves = []
                    base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
                    print_grid(base_grid)
            else:
                player_row = int(input("Select a row: "))-1
                player_col = int(input("Select a column: "))-1
                move = (player_row, player_col)
    """
