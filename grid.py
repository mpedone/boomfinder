'''
In the simplest iteration, the game board will be a 10x10 grid of locations, represented by 100 tuples (0,0) through (9,9). I'll create an array of these locations, and then select ten at random to be bombs.

How to get the bombs in place? Ten arrays of ten integers?
'''
import random
import constants

def bomb_placement(width, height, bomb_count, row, col):
    game_board_x = list(range(width))
    game_board_y = list(range(height))
    board = [(x, y) for x in game_board_x for y in game_board_y]
    selection = board.index((row, col))
    sel = board.pop(selection)

    bombs = random.sample(board, bomb_count)
    bomb_grid = [[0 for x in range(width)] for y in range(height)]
    for bomb in bombs:
        bomb_grid[bomb[1]][bomb[0]] = 1
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
    if dist_grid[user_row][user_col] == "*":
        print_grid(dist_grid)
        print("You hit a BOOM! Game over!")
        status = 0
    else:
        base_grid[user_row][user_col] = dist_grid[user_row][user_col]
        # print_grid(base_grid)
    return base_grid, status

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

def move_selection(choice):
    """
    Docstring for move_selection
    
    :param choice: What type of move player would like to take. Can be to reveal a square, flag/mark a square (or unmark it), or clear a region around a square

    revealing a square is already implemented elsewhere, just needs to be moved into functions.

    flagging a square will involve putting a mark on a suspected bomb, and will "lock" that square - it will not be selectable by the user, and won't reveal if user clears the region (or if it was blank and consecutive blank squares are cleared (this functionality is not yet implemented)). If chosen as first move, will not set the bombs placement, but the flags should not influence bomb placement (meaning if the user wants to place all the flags before revealing any squares, there is a tiny-but-not-zero chance all the bombs will be placed under marked squares).

    clearing a region clears the (up to) 8 squares (three on corners, 5 on edges) around the selection. ONLY already cleared squares can be selected, unlike revealing a square. Consecutive empty squares should clear. Any bombs in the surrounding squares trigger a game over. Cannot be chosen as the first move.
    """
    pass

def first_move(row, col):
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
    pass

def other_move(row, col):
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
    pass

def mark_square(row, col):
    """
    Docstring for mark_square
    
    :param row: Row selection
    :param col: Column selection

    This function marks a square which the user suspects is a bomb. This does two things: first, it lowers the count of "bombs remaining to mark" (not yet implemented) by 1, and it "locks" the square. The user will not be able to clear it without unmarking it. Neither "reveal" nor "clear region" should reveal a marked square.

    This function will need to check that the square is within the board, has not already been revealed, whehter it is flagged or not, and how many flags the user has remaining.

    If the selection has been marked, the marked should be removed and remaining flags increased by 1.

    Using all flags does not trigger an end game check. It just means a user can't place any more flags until they unmark a square. If all squares are marked, this option will only unmark a square.
    """
    pass

def unmark_square(row, col):
    """
    Docstring for unmark_square
    
    :param row: Row selection
    :param col: Column selection

    This function unmarks a marked square. This is the only operation that can be done to a marked square.

    Function will need to check that the square is within the board and is marked (if it is marked, it has not been revealed).

    This option should only appear if at least one square has been marked.

    I don't think this is needed, as mark_square() should be able to handle the same functionality.
    """
    pass

def clear_region(row, col, base_grid, dist_grid):
    """
    Docstring for clear_region
    
    :param row: Row selection
    :param col: Column selection

    This function reveals any adjacent unflagged  squares around the selection. Square must have been revealed. Revealed squares behave exactly as in other_move() - if there is no bomb, the distance is revealed; if it is blank, the consectutive blank squares are revealed; if there is a bomb, the game ends.

    Function will need to check that the selected square HAS been previously selected or if it is flagged (for messaging purposes). If this check passes, function will call a modified version of other_move(), in that the game won't ask for another input if the square has already been cleared or is flagged, it just ignores it.

    This option should only appear after the first move.
    """
    height = len(base_grid)-1
    width = len(base_grid[0])-1
    row_range = range(-1, 2)
    col_range = range(-1, 2)

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
            update_grid(base_grid, dist_grid, row+r, col+c)

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
        if not row.isnumeric or int(row)-1 not in [0, len(base_grid)]:
            res += f"Row must be a number between 1 and {len(base_grid)}. "
        if not col.isnumeric or int(col)-1 not in [0, len(base_grid[0])]:
            res += f"Column must be a number between 1 and {len(base_grid[0])}."
        return res
    
    if type == "other_move":
        if not row.isnumeric or int(row)-1 not in [0, len(base_grid)]:
            res += f"Row must be a number between 1 and {len(base_grid)}. "
        if not col.isnumeric or int(col)-1 not in [0, len(base_grid[0])]:
            res += f"Column must be a number between 1 and {len(base_grid[0])}."
        row = int(row) - 1
        col = int(col) - 1
        if base_grid[row][col] != "_":
            res = "clear"
        elif base_grid[row][col] == "F":
            res = "flagged"
        else:
            res = "valid"
        return res
            
def auto_clear(row, col, base_grid, dist_grid):
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
    """
    pass


def main():
    # defaults
    board_width = 6
    board_height = 6
    bombs_raw = (0.00708274 * (board_width * board_height)**1.53966) + 3.85371
    number_of_bombs = int(bombs_raw)
    number_of_safes = board_width * board_height - number_of_bombs
    
    print("Let's Find Some BOOMS!")
    width_entry = input("Set the board width: ")
    if not width_entry.isnumeric():
        print("Invalid entry, using default")
    else:
        board_width = int(width_entry)    
    height_entry = input("Set the board height: ")
    if not height_entry.isnumeric():
        print("Invalid entry, using default")
    else:
        board_height = int(height_entry)
    bombs_entry = input("How many BOOMS? ")
    if not bombs_entry.isnumeric():
        print("BOOMS calculated automatically")
        bombs_raw = (0.00708274 * (board_width * board_height)**1.53966) + 3.85371
        number_of_bombs = int(bombs_raw)
    else:
        number_of_bombs = int(bombs_entry)

    
    print(f"BOOMS to avoid: {number_of_bombs}")
    number_of_safes = board_width * board_height - number_of_bombs

    base_grid = [['_' for x in range(board_width)] for y in range(board_height)]

    # moves = [] # list of player moves
    # print_grid(base_grid)
    status = 1
    continue_game = 1
    moves = 0

    while continue_game == 1:
        print_grid(base_grid)
        print(f"{moves=}")
        user_input = input("Select a square: ")
        row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]

        # if len(moves) < 1:
        if moves == 0:
            # player_row = int(input("Select a row: "))-1
            # player_col = int(input("Select a column: "))-1
            # move = (player_row, player_col)
            
            valid_move = validate_input(row_input, col_input, "first_move", base_grid)
            print(f"first move {valid_move}")    
            while valid_move != "":
                user_input = input("Select a square: ")
                row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
                valid_move = validate_input(row_input, col_input, "first_move", base_grid)
            player_row, player_col = int(row_input)-1, int(col_input)-1
            # move = (player_row, player_col)
            bomb_grid = bomb_placement(board_width, board_height, number_of_bombs, player_row, player_col)
            dist_grid = calc_dist(board_width, board_height, bomb_grid)
            # moves.append(move)
            base_grid, status = update_grid(base_grid, dist_grid, player_row, player_col)
            moves += 1
        else:
            if status == 1:
                if moves == number_of_safes:
                    print("All spaces cleared! You win!")
                    cont = input("Would you like to play again? ").lower()
                    if cont == "n" or cont == "no":
                        continue_game = 0
                    else:
                        moves = 0
                        base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
                        print_grid(base_grid)
                else:
                    valid_move = validate_input(row_input, col_input, "other_move", base_grid)
                    while valid_move not in ["valid", "clear", "flagged"]:
                        print(valid_move)
                        user_input = input("Select a square: ")
                        row_input, col_input = user_input.split(",")[0], user_input.split(",")[1]
                        valid_move = validate_input(row_input, col_input, "other_move", base_grid)
                        
                    player_row, player_col = int(row_input)-1, int(col_input)-1

                    if valid_move == "clear":
                        clear_region(player_row, player_col, base_grid, dist_grid)
                        moves += 1
                    elif valid_move == "flagged":
                        pass
                    elif valid_move == "valid":
                        # move = {player_row, player_col}
                        # moves.append(move)
                        base_grid, status = update_grid(base_grid, dist_grid, player_row, player_col)
                        moves += 1

        # while move in moves:
        #     print("Square already selected. Please select again.")
        #     player_row = int(input("Select a row: "))-1
        #     player_col = int(input("Select a column: "))-1
        #     # clear_region(player_row, player_col, base_grid, dist_grid)
        #     move = (player_row, player_col)
        
        
        


        # if status == 1:
        #     if len(moves) == number_of_safes:
        #         print("All spaces cleared! You win!")
        #         cont = input("Would you like to play again? ").lower()
        #         if cont == "n" or cont == "no":
        #             continue_game = 0
        #         else:
        #             moves = []
        #             base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
        #             print_grid(base_grid)
        #     else:
        #         player_row = int(input("Select a row: "))-1
        #         player_col = int(input("Select a column: "))-1
        #         move = (player_row, player_col)
        if status == 0:
            cont = input("Would you like to play again? ").lower()
            if cont == "n" or cont == "no":
                continue_game = 0
            else:
                status == 1
                moves = []
                base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
                print_grid(base_grid)    

if __name__ == "__main__":
    main()
