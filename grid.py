'''
In the simplest iteration, the game board will be a 10x10 grid of locations, represented by 100 tuples (0,0) through (9,9). I'll create an array of these locations, and then select ten at random to be bombs.

How to get the bombs in place? Ten arrays of ten integers?
'''
import random

def bomb_placement(board):
    bomb_count = 10
    bomb_locs = []
    for i in range(bomb_count):
        loc = random.choice(board)
        bomb_locs.append(loc) 
        board.pop(board.index(loc))
    return bomb_locs

def print_grid():
    print("   1 2 3 4 5 6 7 8 9 10")
    print(" 1 . . . . . . . . . .")
    print(" 2 . . . . . . . . . .")
    print(" 3 . . . . . . . . . .")
    print(" 4 . . . . . . . . . .")
    print(" 5 . . . . . . . . . .")
    print(" 6 . . . . . . . . . .")
    print(" 7 . . . . . . . . . .")
    print(" 8 . . . . . . . . . .")
    print(" 9 . . . . . . . . . .")
    print("10 . . . . . . . . . .")



def main():
    game_board_x = list(range(10))
    game_board_y = list(range(10))

    game_board = [(x, y) for x in game_board_x for y in game_board_y]
    bombs = bomb_placement(game_board)
    print_grid()
    print(bombs)

if __name__ == "__main__":
    main()
