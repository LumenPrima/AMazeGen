import random

def generate_growing_tree(maze, selection_method='random'):
    width, height = maze.width, maze.height
    grid = maze.grid

    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    grid[y * 2 + 1][x * 2 + 1] = 0
    cells = [(x, y)]

    while cells:
        if selection_method == 'newest':
            index = -1
        elif selection_method == 'random':
            index = random.randint(0, len(cells) - 1)
        elif selection_method == 'oldest':
            index = 0
        else:
            index = -1  # Default to newest

        x, y = cells[index]
        directions = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny * 2 + 1][nx * 2 + 1] == 1:
                directions.append((dx, dy))

        if directions:
            dx, dy = random.choice(directions)
            nx, ny = x + dx, y + dy
            # Remove wall between cells
            grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
            grid[ny * 2 + 1][nx * 2 + 1] = 0
            cells.append((nx, ny))
        else:
            cells.pop(index)
