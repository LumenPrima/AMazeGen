import random

def generate_quad_tree_maze(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    def divide(x, y, w, h):
        if w <= 2 or h <= 2:
            return

        # Divide the current rectangle into four quadrants
        divide_x = x + w // 2
        divide_y = y + h // 2

        # Create passages between quadrants
        passages = random.sample([
            (divide_x, y + random.randint(0, h // 2 - 1)),
            (divide_x, y + h // 2 + random.randint(0, h // 2 - 1)),
            (x + random.randint(0, w // 2 - 1), divide_y),
            (x + w // 2 + random.randint(0, w // 2 - 1), divide_y)
        ], 2)

        for px, py in passages:
            if 0 <= py * 2 + 1 < height * 2 + 1 and 0 <= px * 2 + 1 < width * 2 + 1:
                grid[py * 2 + 1][px * 2 + 1] = 0

        # Recursively divide the quadrants
        divide(x, y, w // 2, h // 2)
        divide(divide_x, y, w - w // 2, h // 2)
        divide(x, divide_y, w // 2, h - h // 2)
        divide(divide_x, divide_y, w - w // 2, h - h // 2)

    # Initialize the grid with all walls
    for y in range(height * 2 + 1):
        for x in range(width * 2 + 1):
            grid[y][x] = 1

    # Start the recursive division
    divide(0, 0, width, height)

    # Ensure the grid cells are passages
    for y in range(height):
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0

    # Ensure outer walls are intact
    for x in range(width * 2 + 1):
        grid[0][x] = 1
        grid[height * 2][x] = 1
    for y in range(height * 2 + 1):
        grid[y][0] = 1
        grid[y][width * 2] = 1

    # Create entrance and exit
    grid[1][0] = 0  # entrance
    grid[height * 2 - 1][width * 2] = 0  # exit
