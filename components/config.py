import pygame

BACKGROUND = (255, 255, 255)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 820

# Grid data
BLOCK_SIZE = 10  # Set the size of the grid block
X_RANGE = int(WINDOW_WIDTH / BLOCK_SIZE)  # 40
Y_RANGE = int((WINDOW_HEIGHT - 100) / BLOCK_SIZE)  # 35
GRID_DATA = [[0 for i in range(X_RANGE)] for j in range(Y_RANGE)]


SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

