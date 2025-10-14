'''
In the simplest iteration, the game board will be a 10x10 grid of locations, represented by 100 tuples (0,0) through (9,9). I'll create an array of these locations, and then select ten at random to be bombs.
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


def main():
    game_board_x = list(range(10))
    game_board_y = list(range(10))

    game_board = [(x, y) for x in game_board_x for y in game_board_y]
    bombs = bomb_placement(game_board)
    print(bombs)

if __name__ == "__main__":
    main()
