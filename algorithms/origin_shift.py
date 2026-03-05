import random


def generate_origin_shift(maze):
    """Origin Shift algorithm: iteratively mutate a spanning tree by shifting
    the root to random neighbors. Converges to a uniform random spanning tree.
    """
    width, height = maze.width, maze.height
    grid = maze.grid

    # Initialize: simple spanning tree where every cell points toward (0,0)
    # Left column points up, everything else points left
    direction = [[None] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if y == 0 and x == 0:
                direction[y][x] = None  # root
            elif x > 0:
                direction[y][x] = (0, -1)  # west
            else:
                direction[y][x] = (-1, 0)  # north

    root_y, root_x = 0, 0
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    iterations = width * height * 5

    for _ in range(iterations):
        # Pick a random neighbor of the root
        random.shuffle(dirs)
        for dy, dx in dirs:
            ny, nx = root_y + dy, root_x + dx
            if 0 <= ny < height and 0 <= nx < width:
                # Root points toward neighbor
                direction[root_y][root_x] = (dy, dx)
                # Neighbor becomes new root (lose its direction)
                direction[ny][nx] = None
                root_y, root_x = ny, nx
                break

    # Convert spanning tree to maze grid
    for y in range(height):
        for x in range(width):
            cy, cx = y * 2 + 1, x * 2 + 1
            grid[cy][cx] = 0
            d = direction[y][x]
            if d is not None:
                dy, dx = d
                grid[cy + dy][cx + dx] = 0
