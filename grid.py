'''
In the simplest iteration, the game board will be a 10x10 grid of locations, represented by 100 tuples (0,0) through (9,9). I'll create an array of these locations, and then select ten at random to be bombs.

How to get the bombs in place? Ten arrays of ten integers?
'''
import random

def bomb_placement(width, height, bomb_count):
    game_board_x = list(range(width))
    game_board_y = list(range(height))
    board = [(x, y) for x in game_board_x for y in game_board_y]

    bombs = random.sample(board, bomb_count)
    # print(bombs)
    bomb_grid = [[0 for x in range(width)] for y in range(height)]
    for bomb in bombs:
        bomb_grid[bomb[1]][bomb[0]] = 1
    return bomb_grid

def print_grid(grid):
    # print("   1 2 3 4 5 6 7 8 9 10")
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
    dist_grid = [[0 for x in range(width)] for y in range(height)]
    for y in range(len(bomb_grid)):
        for x in range(len(bomb_grid[y])):
            if bomb_grid[y][x] == 1:
                dist_grid[y][x] += 9
            elif y == 0:
                if x == 0:
                    dist_grid[y][x] += (bomb_grid[y][x+1] + bomb_grid[y+1][x] + bomb_grid[y+1][x+1])
                elif x == width - 1:
                    dist_grid[y][x] += (bomb_grid[y][x-1] + bomb_grid[y+1][x-1] + bomb_grid[y+1][x])
                else:
                    dist_grid[y][x] += (bomb_grid[y][x-1] + bomb_grid[y][x+1] + bomb_grid[y+1][x-1] + bomb_grid[y+1][x] + bomb_grid[y+1][x+1])
            elif y == height - 1:
                if x == 0:
                    dist_grid[y][x] += (bomb_grid[y-1][x] + bomb_grid[y-1][x+1] + bomb_grid[y][x+1])
                elif x == width - 1:
                    dist_grid[y][x] += (bomb_grid[y-1][x-1] + bomb_grid[y-1][x] + bomb_grid[y][x-1])
                else:
                    dist_grid[y][x] += (bomb_grid[y-1][x-1] + bomb_grid[y-1][x] + bomb_grid[y-1][x+1] + bomb_grid[y][x-1] + bomb_grid[y][x+1])
            elif x == 0:
                dist_grid[y][x] += (bomb_grid[y-1][x] + bomb_grid[y-1][x+1] + bomb_grid[y][x+1] + bomb_grid[y+1][x] + bomb_grid[y+1][x+1])
            elif x == width - 1:
                dist_grid[y][x] += (bomb_grid[y-1][x-1] + bomb_grid[y-1][x] + bomb_grid[y][x-1] + bomb_grid[y+1][x-1] + bomb_grid[y+1][x])
            else:
                dist_grid[y][x] += (bomb_grid[y-1][x-1] + bomb_grid[y-1][x] + bomb_grid[y-1][x+1] + bomb_grid[y][x-1] + bomb_grid[y][x+1] + bomb_grid[y+1][x-1] + bomb_grid[y+1][x] + bomb_grid[y+1][x+1])

    return dist_grid

def main():
    # defaults
    board_width = 9
    board_height = 9
    number_of_bombs = 10
    """
    If we want to dynamically change the number of bombs, we can use an equation (rounded, of course): 
    
    bombs = (0.00708274 * AREA^1.53966) + 3.85371
    """

    base_grid = [['.' for x in range(board_width)] for y in range(board_height)]

    bomb_grid = bomb_placement(board_width, board_height, number_of_bombs)
    dist_grid = calc_dist(board_width, board_height, bomb_grid)

    # print(bombs)
    # print(bomb_grid)
    # print_grid(bomb_grid)
    print_grid(base_grid)

if __name__ == "__main__":
    main()
