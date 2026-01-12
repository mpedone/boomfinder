# import pygame
# import constants
import grid

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
    grid.print_grid(base_grid)
    print(f"{number_of_bombs=}")
    print(f"{number_of_safes=}")


if __name__ == "__main__":
    main()
