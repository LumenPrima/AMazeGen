import random

def generate_ellers(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    sets = [{} for _ in range(height)]
    next_set = 1

    for y in range(height):
        # Assign sets to cells
        for x in range(width):
            if grid[y * 2 + 1][x * 2 + 1] == 1:
                grid[y * 2 + 1][x * 2 + 1] = 0
                sets[y][x] = next_set
                next_set += 1

        # Merge adjacent cells horizontally
        for x in range(width - 1):
            if random.choice([True, False]) or sets[y][x] == sets[y][x + 1]:
                continue
            grid[y * 2 + 1][x * 2 + 2] = 0  # Remove right wall
            old_set = sets[y][x + 1]
            for k in range(width):
                if sets[y][k] == old_set:
                    sets[y][k] = sets[y][x]

        # Prepare for vertical connections
        if y < height - 1:
            # Decide which cells will connect downward
            set_cells = {}
            for x in range(width):
                cell_set = sets[y][x]
                set_cells.setdefault(cell_set, []).append(x)
            for cell_set, cells in set_cells.items():
                connect_down = random.sample(cells, random.randint(1, len(cells)))
                for x in cells:
                    if x in connect_down:
                        grid[y * 2 + 2][x * 2 + 1] = 0  # Remove bottom wall
                        sets[y + 1][x] = cell_set  # Carry set down
                    else:
                        sets[y + 1][x] = None
        else:
            # Last row: ensure all cells are connected
            for x in range(width - 1):
                if sets[y][x] != sets[y][x + 1]:
                    grid[y * 2 + 1][x * 2 + 2] = 0  # Remove right wall
                    old_set = sets[y][x + 1]
                    for k in range(width):
                        if sets[y][k] == old_set:
                            sets[y][k] = sets[y][x]
