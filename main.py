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
    
    status = 1
    continue_game = 1
    new_game = 1
    moves = 0
    cleared = 0
    
    
    while continue_game == 1:

        if new_game:
            board_width, board_height, number_of_bombs, number_of_safes = grid.intialize_grid(board_width, board_height)
            # flags = number_of_bombs
            new_game = 0
       
        if moves == 0:
            base_grid = [['_' for x in range(board_width)] for y in range(board_height)]
            flags = number_of_bombs
        
        print("\n")
        grid.print_grid(base_grid)
        print(f"Flags Remaining: {flags}")
        print(f"Spaces Cleared: {cleared}")
        print(f"Spaces Remaining: {number_of_safes - cleared}\n")

        selection = None
        print("What type of move would you like to make?")
        if moves == 0:
            while selection not in ["r", "f", "q", "h"]:
                selection = input("(R)eveal, (F)lag/Unflag, (H)elp: ")[0].lower()
        else:
            while selection not in ["r", "c", "f", "q", "h"]:
                selection = input("(R)eveal, (C)lear, (F)lag/Unflag, (H)elp: ")[0].lower()
        if selection == "q":
            sys.exit(1)
        if selection == "h":
            grid.instructions()
            input("(press enter to continue)")
            continue
        valid = 0
        user_row, user_col, valid = grid.square_select(base_grid, selection)
        if valid == 0:
            continue

        if selection == "f":
            flags = grid.mark_square(user_row, user_col, base_grid, flags)
        elif selection == "r": # or selection == "c":
            if moves == 0:
                base_grid, status, dist_grid, moves, cleared = grid.first_move(user_row, user_col, board_width, board_height, number_of_bombs, base_grid)
            else:
                base_grid, status = grid.update_grid(base_grid, dist_grid, user_row, user_col)
        elif selection == "c":
            base_grid, status = grid.clear_region(user_row, user_col, base_grid, dist_grid, status)
        cleared = (board_width * board_height) - grid.grid_count(base_grid)

        if cleared == number_of_safes and status == 1:
            base_grid = grid.check_flags(base_grid, dist_grid)
            grid.print_grid(base_grid)
            print("All spaces cleared! You win!")
            status = 0
            """ cont = ""
            while cont not in ["y", "n"]:
                cont = input("Would you like to play again? [y/n] ")[0].lower()
            if cont == "n" or cont == "no":
                continue_game = 0
            else:
                reset_game = input("Reset board? [y/n] ")[0].lower()
                if reset_game == "y":
                    new_game = 1
                moves = 0
                cleared = 0
                flags = number_of_bombs
                base_grid = [['_' for x in range(board_width)] for y in range(board_height)] """
        if status == 0:
            status, moves, cleared, new_game, continue_game = grid.continue_game(new_game)
            """ cont = ""
            while cont not in ["y", "n"]:
                cont = input("Would you like to play again? [y/n] ")[0].lower()
            if cont == "n":
                continue_game = 0
            else:
                reset_game = input("Reset board? [y/n] ")[0].lower()
                if reset_game == "y":
                    new_game = 1
                status = 1
                moves = 0
                cleared = 0
                flags = number_of_bombs
                base_grid = [['_' for x in range(board_width)] for y in range(board_height)] """



if __name__ == "__main__":
    main()
