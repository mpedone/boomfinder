# import pygame
# import constants
import grid
import sys

def main():
    """ pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    x = 615
    y = 335
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x -= 25
                y -= 25
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_UP:
                    y -= 50
                elif event.key == pygame.K_DOWN:
                    y += 50
                elif event.key == pygame.K_LEFT:
                    x -= 50
                elif event.key == pygame.K_RIGHT:
                    x += 50

        pygame.Surface.fill(screen, (128, 128, 128))
        pygame.draw.rect(screen,(255,0,128),(x,y,50,50))
        pygame.display.flip()
        clock.tick(60) """
    board_width = 6
    board_height = 6
    # bombs_raw = (0.00708274 * (board_width * board_height)**1.53966) + 3.85371
    # number_of_bombs = int(bombs_raw)
    # number_of_safes = board_width * board_height - number_of_bombs
    
    board_width, board_height, number_of_bombs, number_of_safes = grid.intialize_grid(board_width, board_height)
    
    base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
    status = 1
    continue_game = 1
    moves = 0
    cleared = 0
    flags = number_of_bombs
    
    while continue_game == 1:
        grid.print_grid(base_grid)
        print(f"Flags Remaining: {flags}")
        print(f"Spaces Cleared: {cleared}")
        print(f"Spaces Remaining: {number_of_safes - cleared}")

        selection = None
        print("What type of move would you like to make?")
        if moves == 0:
            while selection not in ["r", "f", "q"]:
                selection = input("(R)eveal, (F)lag/Unflag: ")[0].lower()
        else:
            while selection not in ["r", "c", "f", "q"]:
                selection = input("(R)eveal, (C)lear, (F)lag/Unflag: ")[0].lower()
        if selection == "q":
            sys.exit(1)
        if selection == "f":
            flags = grid.mark_square(base_grid, flags)
        if selection == "r" or selection == "c":
            if moves == 0:
                base_grid, status, dist_grid, moves, cleared = grid.first_move(board_width, board_height, number_of_bombs, base_grid)
            else:
                base_grid, status, cleared, moves = grid.other_move(board_width, board_height, base_grid, dist_grid, status, moves)
            if cleared == number_of_safes and status == 1:
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



if __name__ == "__main__":
    main()
