import random
from disjoint_set import DisjointSet

def generate_kruskal_weighted(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    # Initialize disjoint sets
    ds = DisjointSet([(x, y) for x in range(width) for y in range(height)])

    # Create all possible edges with weights
    edges = []
    for x in range(width):
        for y in range(height):
            for dx, dy in [(1, 0), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx < width and ny < height:
                    weight = random.randint(1, 100)  # Assign a random weight
                    edges.append((weight, (x, y), (nx, ny)))

    # Sort edges by weight
    edges.sort()

    # Initialize grid with walls
    for y in range(height * 2 + 1):
        for x in range(width * 2 + 1):
            grid[y][x] = 1

    # Process edges
    for weight, (x1, y1), (x2, y2) in edges:
        if ds.find((x1, y1)) != ds.find((x2, y2)):
            ds.union((x1, y1), (x2, y2))
            wall_x = x1 * 2 + 1 + (x2 - x1)
            wall_y = y1 * 2 + 1 + (y2 - y1)
            grid[wall_y][wall_x] = 0
            grid[y1 * 2 + 1][x1 * 2 + 1] = 0
            grid[y2 * 2 + 1][x2 * 2 + 1] = 0
