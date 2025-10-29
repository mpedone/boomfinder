'''
In the simplest iteration, the game board will be a 10x10 grid of locations, represented by 100 tuples (0,0) through (9,9). I'll create an array of these locations, and then select ten at random to be bombs.

How to get the bombs in place? Ten arrays of ten integers?
'''
import random

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
        print_grid(base_grid)
    return base_grid, status

def validate_input(entry, type):
    pass

def main():
    # defaults
    board_width = 6
    board_height = 6
    number_of_bombs = 5
    number_of_safes = board_width * board_height - number_of_bombs
    """
    If we want to dynamically change the number of bombs, we can use an equation (rounded, of course): 
    
    bombs = (0.00708274 * AREA^1.53966) + 3.85371
    """
    print("Let's Find Some BOOMS!")
    board_width = int(input("Set the board height: "))
    board_height = int(input("Set the board width: "))
    number_of_bombs = int(input("How many BOOMS? "))
    number_of_safes = board_width * board_height - number_of_bombs

    base_grid = [['_' for x in range(board_width)] for y in range(board_height)]

    moves = [] # list of player moves
    print_grid(base_grid)
    status = 1
    continue_game = 1
    

    while continue_game == 1:
        if len(moves) < 1:
            player_row = int(input("Select a row: "))-1
            player_col = int(input("Select a column: "))-1
            move = (player_row, player_col)
            bomb_grid = bomb_placement(board_width, board_height, number_of_bombs, player_row, player_col)
            dist_grid = calc_dist(board_width, board_height, bomb_grid)

        while move in moves:
            print("Square already selected. Please select again.")
            player_row = int(input("Select a row: "))-1
            player_col = int(input("Select a column: "))-1
            move = (player_row, player_col)
        moves.append(move)
        base_grid, status = update_grid(base_grid, dist_grid, player_row, player_col)
        


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
        if status == 0:
            cont = input("Would you like to play again? ").lower()
            if cont == "n" or cont == "no":
                continue_game = 0
            else:
                status == 1
                moves = []
                base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
                print_grid(base_grid)
            
        

    

    # print(bombs)
    # print(bomb_grid)
    # print_grid(bomb_grid)
    # print_grid(base_grid)
    # print_grid(dist_grid)

    
    

if __name__ == "__main__":
    main()
