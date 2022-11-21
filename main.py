import pygame
from itertools import product

pygame.init()
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ROWS, COLS = 50, 50
CELL_WIDTH, CELL_HEIGHT = WIDTH / COLS, HEIGHT / ROWS


black = (0, 0, 0)
white = (255, 255, 255)


def count_neighbors(x, y, grid) -> int:
    neighbors = []

    for i, j in product(range(-1, 2), range(-1, 2)):
        row = (y + j + len(grid)) % len(grid)
        col = (x + i + len(grid[0])) % len(grid[0])
        neighbors.append(grid[row][col])

    return len(list(filter(lambda x: x == 1, neighbors)))


def draw(grid):
    for i, j in product(range(ROWS), range(COLS), repeat=1):
        color = black
        if grid[i][j] == 1:
            color = white
        pygame.draw.rect(WIN, color, (j * CELL_WIDTH, i *
                         CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


def update(grid):
    next_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    for x, y in product(range(COLS), range(ROWS)):
        count = count_neighbors(x, y, grid)

        if grid[y][x] == 0 and count == 3:
            next_grid[y][x] = 1
        elif grid[y][x] == 1 and (count < 2 or count > 3):
            next_grid[y][x] = 0
        else:
            next_grid[y][x] = grid[y][x]

    return next_grid


def handle_mouse_click(grid, event):
    row = int(event.pos[1] / CELL_HEIGHT)
    col = int(event.pos[0] / CELL_WIDTH)
    grid[row][col] = 1 if grid[row][col] != 1 else 0


def main():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    run = True
    sim_run = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sim_run = not sim_run
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_mouse_click(grid, event)

        draw(grid)
        if sim_run:
            grid = update(grid)
            pygame.display.set_caption("Running...")
        else:
            pygame.display.set_caption("Paused")
        clock.tick(30)
        pygame.display.update()


if __name__ == "__main__":
    main()
