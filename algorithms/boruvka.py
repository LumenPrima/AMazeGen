import random
from disjoint_set import DisjointSet


def generate_boruvka(maze):
    """Boruvka's algorithm: all components simultaneously find their cheapest
    outgoing edge and merge. Produces clustered growth patterns distinct from
    Kruskal's sequential approach.
    """
    width, height = maze.width, maze.height
    grid = maze.grid

    # Assign random weights to all edges
    edges = []
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                edges.append((random.random(), y, x, y, x + 1))
            if y < height - 1:
                edges.append((random.random(), y, x, y + 1, x))

    edges.sort()

    cells = [(y, x) for y in range(height) for x in range(width)]
    ds = DisjointSet(cells)
    num_components = width * height

    # Open all cell positions
    for y in range(height):
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0

    while num_components > 1:
        # Each component finds its cheapest outgoing edge
        cheapest = {}
        for w, y1, x1, y2, x2 in edges:
            c1 = ds.find((y1, x1))
            c2 = ds.find((y2, x2))
            if c1 != c2:
                if c1 not in cheapest or w < cheapest[c1][0]:
                    cheapest[c1] = (w, y1, x1, y2, x2)
                if c2 not in cheapest or w < cheapest[c2][0]:
                    cheapest[c2] = (w, y1, x1, y2, x2)

        if not cheapest:
            break

        # Merge all cheapest edges simultaneously
        for _, (w, y1, x1, y2, x2) in cheapest.items():
            if ds.find((y1, x1)) != ds.find((y2, x2)):
                ds.union((y1, x1), (y2, x2))
                wy = y1 * 2 + 1 + (y2 - y1)
                wx = x1 * 2 + 1 + (x2 - x1)
                grid[wy][wx] = 0
                num_components -= 1
