import random
from disjoint_set import DisjointSet


def generate_percolation(maze):
    """Bond percolation maze: open walls randomly until start connects to finish.

    Produces organic, sparse mazes at the critical percolation threshold.
    Only cells in the connected cluster are opened, giving a natural
    cave-like boundary between passable and impassable regions.
    """
    width, height = maze.width, maze.height
    grid = maze.grid

    # Build list of all internal walls (edges between adjacent cells)
    walls = []
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                walls.append((y, x, y, x + 1))
            if y < height - 1:
                walls.append((y, x, y + 1, x))

    random.shuffle(walls)

    # Track connectivity with union-find
    cells = [(y, x) for y in range(height) for x in range(width)]
    ds = DisjointSet(cells)

    start_cell = (0, 0)
    finish_cell = (height - 1, width - 1)

    # Phase 1: open walls until start and finish are connected
    opened = []
    for wall in walls:
        y1, x1, y2, x2 = wall
        ds.union((y1, x1), (y2, x2))
        opened.append(wall)
        if ds.find(start_cell) == ds.find(finish_cell):
            break

    # Identify cells in the start-finish cluster
    main = ds.find(start_cell)

    # Write to grid: only open cells and walls in the main cluster
    for y in range(height):
        for x in range(width):
            if ds.find((y, x)) == main:
                grid[y * 2 + 1][x * 2 + 1] = 0

    for y1, x1, y2, x2 in opened:
        if ds.find((y1, x1)) == main:
            wy = y1 * 2 + 1 + (y2 - y1)
            wx = x1 * 2 + 1 + (x2 - x1)
            grid[wy][wx] = 0

    # Set start/finish explicitly (top-left and bottom-right of cluster)
    grid[1][1] = 0
    grid[height * 2 - 1][width * 2 - 1] = 0
    maze.start = (1, 1)
    maze.finish = (height * 2 - 1, width * 2 - 1)
