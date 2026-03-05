import random

def generate_quad_tree_maze(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    grid_w = width * 2 + 1
    grid_h = height * 2 + 1

    # Initialize: open all interior cells and passages
    for gy in range(grid_h):
        for gx in range(grid_w):
            if gy == 0 or gy == grid_h - 1 or gx == 0 or gx == grid_w - 1:
                grid[gy][gx] = 1
            elif gy % 2 == 0 and gx % 2 == 0:
                grid[gy][gx] = 1
            else:
                grid[gy][gx] = 0

    def divide(x, y, w, h):
        if w <= 1 or h <= 1:
            return

        # Choose division points in logical cell coordinates
        divide_x = random.randint(x, x + w - 2)
        divide_y = random.randint(y, y + h - 2)

        wall_grid_x = divide_x * 2 + 2  # Vertical wall column
        wall_grid_y = divide_y * 2 + 2  # Horizontal wall row

        # Draw horizontal wall across full width
        for i in range(x, x + w):
            grid[wall_grid_y][i * 2 + 1] = 1

        # Draw vertical wall across full height
        for i in range(y, y + h):
            grid[i * 2 + 1][wall_grid_x] = 1

        # The cross creates 4 wall segments. We need at least 3 passages
        # to ensure all 4 quadrants are connected (spanning tree of 4 nodes).
        segments = []

        # Top segment of vertical wall (connects top-left and top-right)
        top_h = divide_y - y + 1
        if top_h > 0:
            py = random.randint(y, divide_y)
            segments.append((py * 2 + 1, wall_grid_x))

        # Bottom segment of vertical wall (connects bottom-left and bottom-right)
        bottom_h = y + h - divide_y - 1
        if bottom_h > 0:
            py = random.randint(divide_y + 1, y + h - 1)
            segments.append((py * 2 + 1, wall_grid_x))

        # Left segment of horizontal wall (connects top-left and bottom-left)
        left_w = divide_x - x + 1
        if left_w > 0:
            px = random.randint(x, divide_x)
            segments.append((wall_grid_y, px * 2 + 1))

        # Right segment of horizontal wall (connects top-right and bottom-right)
        right_w = x + w - divide_x - 1
        if right_w > 0:
            px = random.randint(divide_x + 1, x + w - 1)
            segments.append((wall_grid_y, px * 2 + 1))

        # Remove exactly 1 random passage to leave 3 openings (if we have all 4)
        if len(segments) >= 4:
            segments.pop(random.randint(0, len(segments) - 1))

        for gy, gx in segments:
            grid[gy][gx] = 0

        # Recurse into 4 quadrants
        divide(x, y, left_w, top_h)
        divide(divide_x + 1, y, right_w, top_h)
        divide(x, divide_y + 1, left_w, bottom_h)
        divide(divide_x + 1, divide_y + 1, right_w, bottom_h)

    divide(0, 0, width, height)
