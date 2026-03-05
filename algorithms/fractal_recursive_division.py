import random

def generate_fractal_recursive_division(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    grid_w = width * 2 + 1
    grid_h = height * 2 + 1

    # Initialize: open all interior cells and passages between them
    for gy in range(grid_h):
        for gx in range(grid_w):
            if gy == 0 or gy == grid_h - 1 or gx == 0 or gx == grid_w - 1:
                grid[gy][gx] = 1  # Border walls
            elif gy % 2 == 0 and gx % 2 == 0:
                grid[gy][gx] = 1  # Pillar positions always walls
            else:
                grid[gy][gx] = 0  # Open cells and passages

    max_depth = max(1, int(min(width, height) * 0.5))

    def divide(x, y, w, h, depth):
        if w <= 1 or h <= 1 or depth <= 0:
            return

        if h > w:
            horizontal = True
        elif w > h:
            horizontal = False
        else:
            horizontal = random.choice([True, False])

        if horizontal:
            # Wall between logical row divide_y and divide_y+1
            divide_y = random.randint(y, y + h - 2)
            wall_grid_y = divide_y * 2 + 2  # Even grid row = wall row

            # Passage at one cell column
            passage_x = random.randint(x, x + w - 1)
            passage_grid_x = passage_x * 2 + 1

            # Draw horizontal wall
            for i in range(x, x + w):
                grid_x = i * 2 + 1
                if grid_x != passage_grid_x:
                    grid[wall_grid_y][grid_x] = 1

            # Recurse into top and bottom halves
            divide(x, y, w, divide_y - y + 1, depth - 1)
            divide(x, divide_y + 1, w, y + h - divide_y - 1, depth - 1)
        else:
            # Wall between logical column divide_x and divide_x+1
            divide_x = random.randint(x, x + w - 2)
            wall_grid_x = divide_x * 2 + 2  # Even grid col = wall col

            # Passage at one cell row
            passage_y = random.randint(y, y + h - 1)
            passage_grid_y = passage_y * 2 + 1

            # Draw vertical wall
            for i in range(y, y + h):
                grid_y = i * 2 + 1
                if grid_y != passage_grid_y:
                    grid[grid_y][wall_grid_x] = 1

            # Recurse into left and right halves
            divide(x, y, divide_x - x + 1, h, depth - 1)
            divide(divide_x + 1, y, x + w - divide_x - 1, h, depth - 1)

    divide(0, 0, width, height, max_depth)
