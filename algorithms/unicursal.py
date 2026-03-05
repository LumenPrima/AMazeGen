import random


def generate_unicursal(maze):
    """Unicursal (labyrinth) maze: a single non-branching path that visits
    every cell exactly once. No dead ends, no decision points.

    Uses Warnsdorf's heuristic (prefer neighbors with fewest exits) to find
    a Hamiltonian path. Falls back to a serpentine pattern if needed.
    """
    width, height = maze.width, maze.height
    grid = maze.grid
    total = width * height

    path = None
    for _ in range(10):
        path = _hamiltonian(width, height)
        if path and len(path) == total:
            break
        path = None

    if path is None:
        path = _serpentine(width, height)

    _write_path(path, grid)

    # Set start/finish to path endpoints
    sy, sx = path[0]
    fy, fx = path[-1]
    maze.start = (sy * 2 + 1, sx * 2 + 1)
    maze.finish = (fy * 2 + 1, fx * 2 + 1)


def _hamiltonian(width, height):
    visited = [[False] * width for _ in range(height)]
    total = width * height

    # Start from a random corner for higher success rate
    sy = random.choice([0, height - 1])
    sx = random.choice([0, width - 1])
    visited[sy][sx] = True
    path = [(sy, sx)]

    while len(path) < total:
        y, x = path[-1]
        nbrs = []
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and not visited[ny][nx]:
                # Warnsdorf: count future unvisited neighbors
                exits = 0
                for ddy, ddx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    eny, enx = ny + ddy, nx + ddx
                    if 0 <= eny < height and 0 <= enx < width and not visited[eny][enx]:
                        exits += 1
                nbrs.append((exits, random.random(), ny, nx))

        if not nbrs:
            return None

        nbrs.sort()
        _, _, ny, nx = nbrs[0]
        visited[ny][nx] = True
        path.append((ny, nx))

    return path


def _serpentine(width, height):
    path = []
    for y in range(height):
        if y % 2 == 0:
            for x in range(width):
                path.append((y, x))
        else:
            for x in range(width - 1, -1, -1):
                path.append((y, x))
    return path


def _write_path(path, grid):
    for i, (cy, cx) in enumerate(path):
        grid[cy * 2 + 1][cx * 2 + 1] = 0
        if i > 0:
            py, px = path[i - 1]
            wy = py * 2 + 1 + (cy - py)
            wx = px * 2 + 1 + (cx - px)
            grid[wy][wx] = 0
