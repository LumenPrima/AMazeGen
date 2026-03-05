import random
from collections import deque

def generate_cellular_automata(maze, generations=4):
    width, height = maze.width * 2 + 1, maze.height * 2 + 1
    grid = maze.grid

    # Initialize grid with random walls, enforcing borders
    for y in range(height):
        for x in range(width):
            if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                grid[y][x] = 1
            else:
                grid[y][x] = 1 if random.random() < 0.4 else 0

    # Apply cellular automata rules
    for _ in range(generations):
        new_grid = [row[:] for row in grid]
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                wall_count = sum(grid[ny][nx] for nx in range(x - 1, x + 2)
                                 for ny in range(y - 1, y + 2) if (nx, ny) != (x, y))
                if wall_count > 4:
                    new_grid[y][x] = 1
                elif wall_count < 4:
                    new_grid[y][x] = 0
        grid[:] = new_grid[:]

    # Enforce borders after automata
    for x in range(width):
        grid[0][x] = 1
        grid[height - 1][x] = 1
    for y in range(height):
        grid[y][0] = 1
        grid[y][width - 1] = 1

    # Set start and finish explicitly so Maze.generate() won't call
    # select_start_finish (which uses distance-2 checks unsuitable for caves)
    grid[1][1] = 0
    grid[height - 2][width - 2] = 0
    maze.start = (1, 1)
    maze.finish = (height - 2, width - 2)

    # Connect all open regions to ensure solvability
    _ensure_connectivity(grid, width, height)

def _ensure_connectivity(grid, width, height):
    """Flood-fill from (1,1) and connect any isolated open regions."""
    visited = [[False] * width for _ in range(height)]
    queue = deque([(1, 1)])
    visited[1][1] = True

    while queue:
        y, x = queue.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 < ny < height - 1 and 0 < nx < width - 1 and not visited[ny][nx] and grid[ny][nx] == 0:
                visited[ny][nx] = True
                queue.append((ny, nx))

    # Find isolated open cells and connect them to the main component
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if grid[y][x] == 0 and not visited[y][x]:
                # BFS from this cell toward a visited cell
                _connect_to_main(grid, visited, y, x, width, height)

def _connect_to_main(grid, visited, start_y, start_x, width, height):
    """Carve a path from an isolated cell to the main connected component."""
    queue = deque([(start_y, start_x, [(start_y, start_x)])])
    seen = {(start_y, start_x)}

    while queue:
        y, x, path = queue.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 < ny < height - 1 and 0 < nx < width - 1 and (ny, nx) not in seen:
                if visited[ny][nx]:
                    # Found the main component — carve the path
                    for py, px in path:
                        grid[py][px] = 0
                        visited[py][px] = True
                    return
                seen.add((ny, nx))
                queue.append((ny, nx, path + [(ny, nx)]))
