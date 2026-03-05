import random
import math

def select_start_finish(maze):
    max_y = maze.height * 2
    max_x = maze.width * 2

    # Define corners
    corners = [
        (1, 1),  # Top-left (Index 0)
        (max_y - 1, max_x - 1),  # Bottom-right (Index 1)
        (1, max_x - 1),  # Top-right (Index 2)
        (max_y - 1, 1),  # Bottom-left (Index 3)
    ]

    # Randomly select start corner
    start_index = random.randint(0, 3)
    start_corner = corners[start_index]

    # Select the diagonally opposite corner for finish
    finish_index = start_index ^ 1  # Diagonally opposite corner
    finish_corner = corners[finish_index]

    # Define the size of the corner regions (10% of the maze size)
    delta_y = max(1, int(maze.height * 2 * 0.1))
    delta_x = max(1, int(maze.width * 2 * 0.1))

    # Function to generate a random position near a corner
    def get_random_near_corner(corner_y, corner_x):
        # Determine y range
        if corner_y == 1:
            y_values = [y for y in range(1, min(max_y, delta_y * 2), 2)]
        else:
            y_values = [y for y in range(max_y - 1, max(max_y - delta_y * 2, 0), -2)]
        
        # Determine x range
        if corner_x == 1:
            x_values = [x for x in range(1, min(max_x, delta_x * 2), 2)]
        else:
            x_values = [x for x in range(max_x - 1, max(max_x - delta_x * 2, 0), -2)]
        
        # Weighting towards the corner
        skew_factor = 2  # Adjust this to change the weighting
        
        # Randomly select y
        y_weights = [((i + 1) ** (-skew_factor)) for i in range(len(y_values))]
        total_weight_y = sum(y_weights)
        y_probs = [w / total_weight_y for w in y_weights]
        y = random.choices(y_values, weights=y_probs, k=1)[0]
        
        # Randomly select x
        x_weights = [((i + 1) ** (-skew_factor)) for i in range(len(x_values))]
        total_weight_x = sum(x_weights)
        x_probs = [w / total_weight_x for w in x_weights]
        x = random.choices(x_values, weights=x_probs, k=1)[0]
        
        return y, x

    # Get start point near the selected corner
    sy, sx = get_random_near_corner(*start_corner)
    maze.start = (sy, sx)
    # Ensure the start cell is open
    maze.grid[sy][sx] = 0

    # Get finish point near the diagonally opposite corner
    fy, fx = get_random_near_corner(*finish_corner)
    maze.finish = (fy, fx)
    # Ensure the finish cell is open
    maze.grid[fy][fx] = 0

    # Ensure start and finish are connected to the maze
    for point in [maze.start, maze.finish]:
        y, x = point
        # Get adjacent cell positions (moving by 2 units to stay on cells)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        random.shuffle(directions)
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            wall_y, wall_x = y + dy // 2, x + dx // 2
            if 0 < ny < max_y and 0 < nx < max_x and maze.grid[ny][nx] == 0:
                maze.grid[wall_y][wall_x] = 0  # Open wall between cells
                break  # Path is carved, exit the loop

def calculate_difficulty(maze):
    """Calculate maze difficulty as a size-independent score from 0.0 to 1.0.

    Components (all normalized ratios):
      - Path indirectness: how much longer the solution is vs manhattan distance
      - Dead end density: fraction of cells that are traps
      - Decision density: fraction of solution steps where solver must choose
      - Turn density: fraction of solution steps with direction changes
    """
    path = maze.find_path()
    if not path:
        return 0.0

    path_length = len(path)
    grid = maze.grid
    grid_h = len(grid)
    grid_w = len(grid[0])

    # Manhattan distance between start and finish (grid coordinates)
    manhattan = abs(maze.start[0] - maze.finish[0]) + abs(maze.start[1] - maze.finish[1])
    if manhattan == 0:
        return 0.0

    # --- Maze-wide metrics ---
    total_open_cells = 0
    dead_ends = 0
    for y in range(maze.height):
        for x in range(maze.width):
            cy, cx = y * 2 + 1, x * 2 + 1
            if grid[cy][cx] == 0:
                total_open_cells += 1
                walls_open = 0
                for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if grid[cy + dy][cx + dx] == 0:
                        walls_open += 1
                if walls_open == 1:
                    dead_ends += 1

    if total_open_cells == 0:
        return 0.0

    # --- Path metrics ---
    # Decision points: path cells with > 2 open grid neighbors (must choose)
    decisions = 0
    for r, c in path:
        neighbors = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid_h and 0 <= nc < grid_w and grid[nr][nc] == 0:
                neighbors += 1
        if neighbors > 2:
            decisions += 1

    # Turn count: direction changes along the path
    turns = 0
    for i in range(2, path_length):
        d1 = (path[i-1][0] - path[i-2][0], path[i-1][1] - path[i-2][1])
        d2 = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])
        if d1 != d2:
            turns += 1

    # --- Normalized components, each scaled to [0, 1] ---

    # Path indirectness: how winding is the solution relative to straight line?
    total_open_grid = sum(1 for row in grid for c in row if c == 0)
    max_path = max(total_open_grid, manhattan + 1)
    indirectness = (path_length - manhattan) / max(max_path - manhattan, 1)
    indirectness = min(max(indirectness, 0.0), 1.0)

    # Dead end density (perfect mazes peak ~0.5, so *2 to normalize to ~1.0)
    dead_end_score = min(dead_ends / total_open_cells * 2, 1.0)

    # Decision density along solution (typically 0–0.3, so *3 to normalize)
    decision_score = min(decisions / path_length * 3, 1.0)

    # Turn density along solution
    turn_score = turns / max(path_length - 1, 1)

    # --- Weighted combination → [0, 1] ---
    difficulty = (
        indirectness   * 0.35 +
        dead_end_score * 0.25 +
        decision_score * 0.25 +
        turn_score     * 0.15
    )

    return round(difficulty, 4)
