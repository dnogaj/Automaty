import pygame
import sys
import numpy
from game_of_life_alg import omnipresent_perception, next_matrix, ar_insert
from photo_refactor import black_and_white


pygame.init()

cell_size = 10
N = 100
width, height = N * cell_size, N * cell_size
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Of Life")

black = (0, 0, 0)
white = (200, 200, 200)
grey = (169, 169, 169)

initial_board = black_and_white("3.jpg", "11.jpg", N)

matrix = initial_board
testarr = numpy.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
ar_insert(matrix, testarr, 10, 10)
data = omnipresent_perception()
dead_or_alive = data[0]
arr = data[1]

drawing = False

continuos_sim = 0
tick = 40


# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Handle mouse events for drawing live cells
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                x, y = event.pos
                col = x // cell_size % N
                row = y // cell_size % N
                matrix[row, col] = 1
        elif event.type == pygame.MOUSEMOTION and drawing:
            x, y = event.pos
            col = x // cell_size % N
            row = y // cell_size % N
            matrix[row, col] = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            matrix = next_matrix(matrix, N, dead_or_alive, arr)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            matrix[:,:] = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
            if tick > 6:
                tick = tick - 5
            print(tick)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
            if tick < 55:
                tick = tick + 5

            print (tick)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F10:
            continuos_sim =- continuos_sim + 1

    if continuos_sim == 1:
        matrix = next_matrix(matrix, N, dead_or_alive, arr)

    window.fill(white)

    # Draw live cells with borders
    for i in range(N):
        for j in range(N):
            if matrix[i, j] == 1:
                rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                pygame.draw.rect(window, black, rect)

    for i in range(N + 1):
        pygame.draw.line(window, grey, (i * cell_size, 0), (i * cell_size, height), 1)
        pygame.draw.line(window, grey, (0, i * cell_size), (width, i * cell_size), 1)

    pygame.display.flip()

    pygame.time.Clock().tick(tick)
