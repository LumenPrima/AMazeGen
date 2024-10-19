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
    path = maze.find_path()
    if not path:
        return 0  # No solution, so difficulty is 0

    path_length = len(path)

    # Total number of cells (excluding walls)
    total_cells = maze.width * maze.height

    # Calculate path difficulty: longer paths in larger mazes should be more difficult
    path_difficulty = path_length / (2 * total_cells - 1) if total_cells > 0 else 0

    # Initialize counters
    dead_ends = 0
    intersections = 0
    total_open_cells = 0
    total_branches = 0

    for y in range(maze.height):
        for x in range(maze.width):
            cell_y, cell_x = y * 2 + 1, x * 2 + 1
            if maze.grid[cell_y][cell_x] == 0:
                total_open_cells += 1
                # Count open neighbors
                open_neighbors = 0
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < maze.width and 0 <= ny < maze.height:
                        neighbor_cell_y, neighbor_cell_x = ny * 2 + 1, nx * 2 + 1
                        if maze.grid[neighbor_cell_y][neighbor_cell_x] == 0:
                            open_neighbors += 1
                total_branches += open_neighbors
                if open_neighbors == 1:
                    dead_ends += 1
                elif open_neighbors > 2:
                    intersections += 1

    # Avoid division by zero
    if total_open_cells == 0:
        return 0

    # Dead-end fraction
    dead_end_fraction = dead_ends / total_open_cells

    # Intersection fraction
    intersection_fraction = intersections / total_open_cells

    # Average branching factor (normalized)
    average_branching_factor = (total_branches / total_open_cells) / 4  # Max possible branching is 4

    # Maze density (normalized)
    wall_cells = sum(1 for row in maze.grid for cell in row if cell == 1)
    possible_walls = len(maze.grid) * len(maze.grid[0])
    density = wall_cells / possible_walls

    # Calculate straight line penalty
    straight_line_penalty = calculate_straight_line_penalty(path)

    # Combine metrics into a difficulty score
    difficulty = (
        0.40 * path_difficulty +         # Emphasize path length
        0.20 * dead_end_fraction +       # Dead ends contribute to difficulty
        0.15 * intersection_fraction +   # Intersections increase complexity
        0.15 * average_branching_factor + # More choices increase difficulty
        0.10 * straight_line_penalty     # Penalize long straight lines
    )

    return difficulty

def calculate_straight_line_penalty(path):
    if not path or len(path) < 3:
        return 0

    straight_line_segments = []
    current_segment = [path[0], path[1]]
    current_direction = (path[1][0] - path[0][0], path[1][1] - path[0][1])

    for i in range(2, len(path)):
        new_direction = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])
        if new_direction == current_direction:
            current_segment.append(path[i])
        else:
            if len(current_segment) > 2:
                straight_line_segments.append(current_segment)
            current_segment = [path[i-1], path[i]]
            current_direction = new_direction

    if len(current_segment) > 2:
        straight_line_segments.append(current_segment)

    # Calculate penalty based on the length of straight line segments
    total_path_length = len(path)
    straight_line_length = sum(len(segment) for segment in straight_line_segments)
    straight_line_ratio = straight_line_length / total_path_length

    # Apply a more severe penalty for higher ratios of straight lines
    penalty = math.pow(straight_line_ratio, 2)  # Quadratic penalty

    return penalty
