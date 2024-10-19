import random

def generate_cellular_automata(maze, generations=4):
    width, height = maze.width * 2 + 1, maze.height * 2 + 1
    grid = maze.grid

    # Initialize grid with random walls
    for y in range(height):
        for x in range(width):
            grid[y][x] = 1 if random.random() < 0.4 else 0

    # Apply cellular automata rules
    for _ in range(generations):
        new_grid = [row[:] for row in grid]
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                wall_count = sum(grid[ny][nx] for nx in range(x - 1, x + 2)
                                 for ny in range(y - 1, y + 2) if (nx, ny) != (x, y))
                if wall_count > 4:
                    new_grid[y][x] = 1
                elif wall_count < 4:
                    new_grid[y][x] = 0
        grid[:] = new_grid[:]

    # Ensure start and finish are open
    grid[1][1] = 0
    grid[height - 2][width - 2] = 0
