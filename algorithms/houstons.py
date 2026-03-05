import random


def generate_houstons(maze):
    """Houston's algorithm: hybrid Aldous-Broder + Wilson's.

    Phase 1 (Aldous-Broder): random walk, recording first-visit edges,
    until ~30% of cells are visited. Fast when most cells are unvisited.

    Phase 2 (Wilson's): loop-erased random walks from remaining unvisited
    cells to the visited set. Fast when most cells are already visited.
    """
    width, height = maze.width, maze.height
    grid = maze.grid
    total = width * height

    visited = [[False] * width for _ in range(height)]
    parent = [[None] * width for _ in range(height)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Phase 1: Aldous-Broder until ~30% visited
    threshold = max(1, int(total * 0.3))
    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    visited[y][x] = True
    count = 1

    while count < threshold:
        dy, dx = random.choice(dirs)
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            if not visited[ny][nx]:
                visited[ny][nx] = True
                parent[ny][nx] = (y, x)
                count += 1
            x, y = nx, ny

    # Phase 2: Wilson's loop-erased random walk for the rest
    for sy in range(height):
        for sx in range(width):
            if visited[sy][sx]:
                continue

            # Random walk from (sx, sy) until hitting visited set
            walk = {}
            cy, cx = sy, sx
            while not visited[cy][cx]:
                dy, dx = random.choice(dirs)
                ny, nx = cy + dy, cx + dx
                if 0 <= nx < width and 0 <= ny < height:
                    walk[(cy, cx)] = (ny, nx)
                    cy, cx = ny, nx

            # Trace loop-erased path and add to tree
            cy, cx = sy, sx
            while not visited[cy][cx]:
                visited[cy][cx] = True
                ny, nx = walk[(cy, cx)]
                parent[cy][cx] = (ny, nx)
                cy, cx = ny, nx

    # Convert parent pointers to maze grid
    for y in range(height):
        for x in range(width):
            cy, cx = y * 2 + 1, x * 2 + 1
            grid[cy][cx] = 0
            if parent[y][x] is not None:
                py, px = parent[y][x]
                grid[cy + (py - y)][cx + (px - x)] = 0
