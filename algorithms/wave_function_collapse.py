import random
from collections import deque

# Direction bitmasks
N, E, S, W = 1, 2, 4, 8

# (bitmask, row_delta, col_delta, opposite_bitmask)
NEIGHBORS = [
    (N, -1, 0, S),
    (E, 0, 1, W),
    (S, 1, 0, N),
    (W, 0, -1, E),
]

# All tiles with at least one opening
ALL_TILES = frozenset(range(1, 16))

# Weights: favor corridors/corners for winding passages
_OPENING_WEIGHTS = {1: 1.0, 2: 3.0, 3: 1.5, 4: 0.3}


def _weight(tile):
    return _OPENING_WEIGHTS[bin(tile).count('1')]


def generate_wave_function_collapse(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    for _ in range(30):
        tiles = _run_wfc(width, height)
        if tiles is not None:
            _write_grid(tiles, grid, width, height)
            _ensure_connectivity(grid, width * 2 + 1, height * 2 + 1)
            return

    # Fallback: DFS spanning tree (always succeeds)
    _write_grid(_fallback_dfs(width, height), grid, width, height)


def _run_wfc(width, height):
    # Initialize possible tile sets per cell
    possible = [[None] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            valid = set()
            for t in ALL_TILES:
                if y == 0 and (t & N):
                    continue
                if y == height - 1 and (t & S):
                    continue
                if x == 0 and (t & W):
                    continue
                if x == width - 1 and (t & E):
                    continue
                valid.add(t)
            possible[y][x] = valid

    while True:
        # Find minimum-entropy uncollapsed cell
        best = None
        best_entropy = float('inf')
        for y in range(height):
            for x in range(width):
                n = len(possible[y][x])
                if n == 0:
                    return None  # Contradiction
                if 1 < n < best_entropy:
                    best_entropy = n
                    best = (y, x)

        if best is None:
            break  # All collapsed

        # Collapse to a weighted random tile
        cy, cx = best
        tiles = list(possible[cy][cx])
        weights = [_weight(t) for t in tiles]
        chosen = random.choices(tiles, weights=weights, k=1)[0]
        possible[cy][cx] = {chosen}

        # Propagate constraints
        if not _propagate(possible, cy, cx, width, height):
            return None

    return [[next(iter(possible[y][x])) for x in range(width)]
            for y in range(height)]


def _propagate(possible, sy, sx, width, height):
    queue = deque([(sy, sx)])
    in_queue = {(sy, sx)}

    while queue:
        y, x = queue.popleft()
        in_queue.discard((y, x))

        for bit, dy, dx, opp in NEIGHBORS:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < height and 0 <= nx < width):
                continue

            can_open = any(t & bit for t in possible[y][x])
            can_close = any(not (t & bit) for t in possible[y][x])

            new_set = set()
            for t in possible[ny][nx]:
                has_opp = bool(t & opp)
                if (has_opp and can_open) or (not has_opp and can_close):
                    new_set.add(t)

            if not new_set:
                return False

            if new_set != possible[ny][nx]:
                possible[ny][nx] = new_set
                if (ny, nx) not in in_queue:
                    queue.append((ny, nx))
                    in_queue.add((ny, nx))

    return True


def _write_grid(tiles, grid, width, height):
    """Convert tile bitmasks to wall-based grid. Only writes S and E walls
    to avoid double-writing (N/W handled by the neighbor's S/E)."""
    for y in range(height):
        for x in range(width):
            tile = tiles[y][x]
            cy, cx = y * 2 + 1, x * 2 + 1
            grid[cy][cx] = 0
            if (tile & S) and y < height - 1:
                grid[cy + 1][cx] = 0
            if (tile & E) and x < width - 1:
                grid[cy][cx + 1] = 0


def _ensure_connectivity(grid, grid_w, grid_h):
    """Flood-fill from first open cell, connect isolated regions."""
    visited = [[False] * grid_w for _ in range(grid_h)]
    queue = deque()

    for y in range(1, grid_h - 1):
        for x in range(1, grid_w - 1):
            if grid[y][x] == 0:
                queue.append((y, x))
                visited[y][x] = True
                break
        if queue:
            break

    while queue:
        y, x = queue.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 < ny < grid_h - 1 and 0 < nx < grid_w - 1 and not visited[ny][nx] and grid[ny][nx] == 0:
                visited[ny][nx] = True
                queue.append((ny, nx))

    for y in range(1, grid_h - 1):
        for x in range(1, grid_w - 1):
            if grid[y][x] == 0 and not visited[y][x]:
                _connect(grid, visited, y, x, grid_w, grid_h)


def _connect(grid, visited, sy, sx, width, height):
    queue = deque([(sy, sx, [(sy, sx)])])
    seen = {(sy, sx)}
    while queue:
        y, x, path = queue.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 < ny < height - 1 and 0 < nx < width - 1 and (ny, nx) not in seen:
                if visited[ny][nx]:
                    for py, px in path:
                        grid[py][px] = 0
                        visited[py][px] = True
                    return
                seen.add((ny, nx))
                queue.append((ny, nx, path + [(ny, nx)]))


def _fallback_dfs(width, height):
    """DFS spanning tree as fallback if WFC repeatedly contradicts."""
    tiles = [[0] * width for _ in range(height)]
    visited = [[False] * width for _ in range(height)]
    y, x = random.randint(0, height - 1), random.randint(0, width - 1)
    visited[y][x] = True
    stack = [(y, x)]
    while stack:
        y, x = stack[-1]
        nbrs = []
        for bit, dy, dx, opp in NEIGHBORS:
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and not visited[ny][nx]:
                nbrs.append((ny, nx, bit, opp))
        if nbrs:
            ny, nx, bit, opp = random.choice(nbrs)
            tiles[y][x] |= bit
            tiles[ny][nx] |= opp
            visited[ny][nx] = True
            stack.append((ny, nx))
        else:
            stack.pop()
    return tiles
