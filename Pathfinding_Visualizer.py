import pygame
# import math
# from queue import PriorityQueue
# from queue import Queue
import Algorithms

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return (self.row, self.col)

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Left
            self.neighbours.append(grid[self.row][self.col - 1])


    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()

                if spot == start:
                    start = None

                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:    # if key is pressed

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_m and start and end:     # if the pressed key is SPACE
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    Algorithms.a_star_m(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_e and start and end:  # if the pressed key is SPACE
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    Algorithms.a_star_e(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_a and start and end:  # if the pressed key is SPACE
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    Algorithms.a_star_c(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_d and start and end:  # if the pressed key is SPACE
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    Algorithms.dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_b and start and end:  # if the pressed key is SPACE
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    Algorithms.bfs(lambda: draw(win, grid, ROWS, width), start, end)

                if event.key == pygame.K_f and start and end:  # if the pressed key is SPACE
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)

                    Algorithms.dfs(lambda: draw(win, grid, ROWS, width), start, end)

    pygame.quit()

main(WIN, WIDTH)


