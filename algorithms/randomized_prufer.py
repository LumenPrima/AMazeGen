import random
from disjoint_set import DisjointSet

def generate_randomized_prufer(maze):
    """Generate a maze using Prufer-sequence-weighted random spanning tree.

    Uses a random Prufer sequence to assign priority weights to cells.
    Cells appearing more frequently in the sequence become connection hubs,
    creating mazes with a distinct branching structure.
    """
    width, height = maze.width, maze.height
    grid = maze.grid
    total = width * height

    # Generate a Prufer sequence to determine cell priorities
    prufer = [random.randint(0, total - 1) for _ in range(total - 2)]
    freq = [0] * total
    for v in prufer:
        freq[v] += 1

    # Collect grid-adjacent edges, prioritized by Prufer frequency
    edges = []
    for y in range(height):
        for x in range(width):
            idx = y * width + x
            if x < width - 1:
                nidx = y * width + (x + 1)
                priority = freq[idx] + freq[nidx] + random.random()
                edges.append((priority, x, y, x + 1, y))
            if y < height - 1:
                nidx = (y + 1) * width + x
                priority = freq[idx] + freq[nidx] + random.random()
                edges.append((priority, x, y, x, y + 1))

    # Sort by priority descending — high-frequency cells get connected first
    edges.sort(reverse=True)

    # Build spanning tree
    ds = DisjointSet([(x, y) for x in range(width) for y in range(height)])

    for _, x1, y1, x2, y2 in edges:
        if ds.find((x1, y1)) != ds.find((x2, y2)):
            ds.union((x1, y1), (x2, y2))
            grid[y1 * 2 + 1][x1 * 2 + 1] = 0
            grid[y2 * 2 + 1][x2 * 2 + 1] = 0
            wall_y = y1 * 2 + 1 + (y2 - y1)
            wall_x = x1 * 2 + 1 + (x2 - x1)
            grid[wall_y][wall_x] = 0
