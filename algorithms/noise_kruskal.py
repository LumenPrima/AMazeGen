import random
from disjoint_set import DisjointSet


def generate_noise_kruskal(maze):
    """Kruskal's algorithm with spatially-correlated noise weights.

    Unlike standard Kruskal (uniform random weights), edges are weighted
    by smooth 2D value noise. This creates regional character: some areas
    have dense, complex passages while others are more open and simple.
    """
    width, height = maze.width, maze.height
    grid = maze.grid

    # Generate smooth noise field over the grid
    grid_w = width * 2 + 1
    grid_h = height * 2 + 1
    scale = max(3, min(width, height) // 4)
    noise = _value_noise(grid_w, grid_h, scale)

    # Build edges with noise-based weights
    edges = []
    for y in range(height):
        for x in range(width):
            if x < width - 1:
                gy, gx = y * 2 + 1, x * 2 + 2
                w = noise[gy][gx] + random.random() * 0.1
                edges.append((w, y, x, y, x + 1))
            if y < height - 1:
                gy, gx = y * 2 + 2, x * 2 + 1
                w = noise[gy][gx] + random.random() * 0.1
                edges.append((w, y, x, y + 1, x))

    edges.sort()

    # Kruskal's MST
    cells = [(y, x) for y in range(height) for x in range(width)]
    ds = DisjointSet(cells)

    for y in range(height):
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0

    for w, y1, x1, y2, x2 in edges:
        if ds.find((y1, x1)) != ds.find((y2, x2)):
            ds.union((y1, x1), (y2, x2))
            wy = y1 * 2 + 1 + (y2 - y1)
            wx = x1 * 2 + 1 + (x2 - x1)
            grid[wy][wx] = 0


def _value_noise(w, h, scale):
    """Smoothstep-interpolated value noise."""
    cw = w // scale + 2
    ch = h // scale + 2
    coarse = [[random.random() for _ in range(cw)] for _ in range(ch)]

    noise = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            fx = x / scale
            fy = y / scale
            ix, iy = int(fx), int(fy)
            dx = fx - ix
            dy = fy - iy

            if ix + 1 < cw and iy + 1 < ch:
                # Smoothstep interpolation
                dx = dx * dx * (3 - 2 * dx)
                dy = dy * dy * (3 - 2 * dy)

                v0 = coarse[iy][ix] + (coarse[iy][ix + 1] - coarse[iy][ix]) * dx
                v1 = coarse[iy + 1][ix] + (coarse[iy + 1][ix + 1] - coarse[iy + 1][ix]) * dx
                noise[y][x] = v0 + (v1 - v0) * dy
            else:
                noise[y][x] = random.random()

    return noise
