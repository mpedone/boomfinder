import pygame
import constants

def main():
    pygame.init()
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
        clock.tick(60)

if __name__ == "__main__":
    main()
