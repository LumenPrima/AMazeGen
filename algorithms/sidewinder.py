import random

def generate_sidewinder(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    for y in range(height):
        run = []
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0
            run.append((x, y))
            carve_east = random.choice([True, False]) if y > 0 else True

            if x == width - 1 or not carve_east:
                # Carve north in the run
                cell_x, cell_y = random.choice(run)
                if cell_y > 0:
                    grid[cell_y * 2][cell_x * 2 + 1] = 0  # Remove north wall
                run = []
            else:
                # Carve east
                grid[y * 2 + 1][x * 2 + 2] = 0  # Remove east wall
