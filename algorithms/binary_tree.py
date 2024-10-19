import random

def generate_binary_tree(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    for y in range(height):
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0
            directions = []
            if x < width - 1:
                directions.append((1, 0))  # East
            if y > 0:
                directions.append((0, -1))  # North
            if directions:
                dx, dy = random.choice(directions)
                nx, ny = x + dx, y + dy
                grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
