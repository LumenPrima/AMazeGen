import random


def generate_recursive_winding(maze):
    """Recursive Winding: the dual of Recursive Division.

    Recursive Division places walls with one passage opening.
    Recursive Winding carves corridors with one wall remaining.

    Produces long open corridors interrupted by single-cell walls,
    the visual inverse of Recursive Division's long walls with gaps.
    """
    width, height = maze.width, maze.height
    grid = maze.grid

    # Open all cell positions
    for y in range(height):
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0

    _wind(grid, 0, 0, width, height)


def _wind(grid, x0, y0, w, h):
    if w < 2 and h < 2:
        return

    if w < 2:
        # Single column: open all internal horizontal walls
        for j in range(h - 1):
            grid[(y0 + j) * 2 + 2][x0 * 2 + 1] = 0
        return

    if h < 2:
        # Single row: open all internal vertical walls
        for i in range(w - 1):
            grid[y0 * 2 + 1][(x0 + i) * 2 + 2] = 0
        return

    if w >= h:
        # Vertical split: carve corridor along a vertical wall column
        sx = random.randint(0, w - 2)
        wall_gx = (x0 + sx) * 2 + 2

        # Open all walls in this column EXCEPT one (leave one blocker)
        positions = list(range(h))
        keep = random.choice(positions)
        for j in positions:
            if j != keep:
                grid[(y0 + j) * 2 + 1][wall_gx] = 0

        _wind(grid, x0, y0, sx + 1, h)
        _wind(grid, x0 + sx + 1, y0, w - sx - 1, h)
    else:
        # Horizontal split: carve corridor along a horizontal wall row
        sy = random.randint(0, h - 2)
        wall_gy = (y0 + sy) * 2 + 2

        positions = list(range(w))
        keep = random.choice(positions)
        for i in positions:
            if i != keep:
                grid[wall_gy][(x0 + i) * 2 + 1] = 0

        _wind(grid, x0, y0, w, sy + 1)
        _wind(grid, x0, y0 + sy + 1, w, h - sy - 1)
