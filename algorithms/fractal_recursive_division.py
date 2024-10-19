import random

def generate_fractal_recursive_division(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    def divide(x, y, w, h, depth):
        if w <= 2 or h <= 2 or depth <= 0:
            return

        # Choose orientation (horizontal or vertical)
        horizontal = True if h > w else False
        if w == h:
            horizontal = random.choice([True, False])

        if horizontal:
            # Choose where to draw the line
            divide_y = random.randint(y + 1, y + h - 2)
            # Choose where to put the passage
            passage_x = random.randint(x, x + w - 1)

            # Draw the horizontal line
            for i in range(x, x + w):
                if i != passage_x:
                    grid[divide_y * 2 + 1][i * 2 + 1] = 1

            # Recursively divide the two new sections
            divide(x, y, w, divide_y - y, depth - 1)
            divide(x, divide_y + 1, w, y + h - divide_y - 1, depth - 1)
        else:
            # Choose where to draw the line
            divide_x = random.randint(x + 1, x + w - 2)
            # Choose where to put the passage
            passage_y = random.randint(y, y + h - 1)

            # Draw the vertical line
            for i in range(y, y + h):
                if i != passage_y:
                    grid[i * 2 + 1][divide_x * 2 + 1] = 1

            # Recursively divide the two new sections
            divide(x, y, divide_x - x, h, depth - 1)
            divide(divide_x + 1, y, x + w - divide_x - 1, h, depth - 1)

    # Initialize the grid with all passages open
    for y in range(height):
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0

    # Add outer walls
    for x in range(width * 2 + 1):
        grid[0][x] = 1
        grid[height * 2][x] = 1
    for y in range(height * 2 + 1):
        grid[y][0] = 1
        grid[y][width * 2] = 1

    # Start the recursive division
    max_depth = int(min(width, height) * 0.5)  # Adjust this value to control the fractal depth
    divide(0, 0, width, height, max_depth)
