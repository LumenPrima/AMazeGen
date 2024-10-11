import random
from collections import deque
import heapq
import math

class Maze:
    def __init__(self, width, height, algorithm):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width * 2 + 1)] for _ in range(height * 2 + 1)]
        self.start = None
        self.finish = None
        self.algorithm = algorithm
                
    def select_start_finish(self):
        max_y = self.height * 2
        max_x = self.width * 2

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
        delta_y = max(1, int(self.height * 2 * 0.1))
        delta_x = max(1, int(self.width * 2 * 0.1))

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
        self.start = (sy, sx)
        # Ensure the start cell is open
        self.grid[sy][sx] = 0

        # Get finish point near the diagonally opposite corner
        fy, fx = get_random_near_corner(*finish_corner)
        self.finish = (fy, fx)
        # Ensure the finish cell is open
        self.grid[fy][fx] = 0

        # Ensure start and finish are connected to the maze
        for point in [self.start, self.finish]:
            y, x = point
            # Get adjacent cell positions (moving by 2 units to stay on cells)
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            random.shuffle(directions)
            for dy, dx in directions:
                ny, nx = y + dy, x + dx
                wall_y, wall_x = y + dy // 2, x + dx // 2
                if 0 < ny < max_y and 0 < nx < max_x and self.grid[ny][nx] == 0:
                    self.grid[wall_y][wall_x] = 0  # Open wall between cells
                    break  # Path is carved, exit the loop


    def to_svg(self, cell_size=10, margin=10):
        width = (self.width * 2 + 1) * cell_size + 2 * margin
        height = (self.height * 2 + 1) * cell_size + 2 * margin
        svg_elements = []

        # Start SVG
        svg_header = f'<svg width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        svg_elements.append(svg_header)
        svg_elements.append('<rect width="100%" height="100%" fill="white"/>')

        # Draw maze walls
        for y in range(self.height * 2 + 1):
            for x in range(self.width * 2 + 1):
                if self.grid[y][x] == 1:
                    wx = margin + x * cell_size
                    wy = margin + y * cell_size
                    svg_elements.append(f'<rect x="{wx}" y="{wy}" width="{cell_size}" height="{cell_size}" fill="black"/>')

        # Draw start and finish points
        if self.start:
            sy, sx = self.start
            cx = margin + sx * cell_size + cell_size // 2
            cy = margin + sy * cell_size + cell_size // 2
            svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{cell_size * 0.4}" fill="green"/>')

        if self.finish:
            fy, fx = self.finish
            cx = margin + fx * cell_size + cell_size // 2
            cy = margin + fy * cell_size + cell_size // 2
            svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{cell_size * 0.4}" fill="red"/>')

        # End SVG
        svg_elements.append('</svg>')

        return '\n'.join(svg_elements)

    def overlay_solution(self, svg_content, cell_size=10, margin=10):
        # Extract the closing SVG tag to append solution before it
        svg_closing_tag = '</svg>'
        if svg_content.endswith(svg_closing_tag):
            svg_content = svg_content[:-len(svg_closing_tag)]
        else:
            # Handle the case where SVG might not end with '</svg>'
            pass

        # Draw solution path
        solution = self.find_path()
        if solution:
            # Calculate path coordinates
            path_coords = [
                (margin + x * cell_size + cell_size // 2, margin + y * cell_size + cell_size // 2)
                for y, x in solution
            ]
            # Build the SVG path string
            path_str = f'M {path_coords[0][0]},{path_coords[0][1]}'
            for x, y in path_coords[1:]:
                path_str += f' L {x},{y}'
            # Add the solution path to SVG
            svg_solution = f'<path d="{path_str}" stroke="blue" stroke-width="{cell_size / 2}" fill="none"/>'

            # Append solution and closing SVG tag
            svg_content += '\n' + svg_solution + '\n</svg>'
        else:
            # If no solution found, just close the SVG
            svg_content += '\n</svg>'

        return svg_content

    def to_svg_with_solution(self, cell_size=10, margin=10):
        # Generate the base maze SVG
        svg_base = self.to_svg(cell_size, margin)

        # Overlay the solution path onto the base SVG
        svg_with_solution = self.overlay_solution(svg_base, cell_size, margin)

        return svg_with_solution
    
    def to_gcode(self, cell_size=10, margin=10, max_size=200, include_solution=False):
        maze_width = (self.width * 2 + 1)
        maze_height = (self.height * 2 + 1)
        scale = max_size / max(maze_width, maze_height)

        # Initialize G-code commands
        gcode_commands = []
        gcode_commands.append('G90')  # Absolute positioning
        gcode_commands.append('G21')  # Units in millimeters
        gcode_commands.append('G0 Z3')  # Pen up

        # Function to convert grid coordinates to plotter coordinates
        def grid_to_plotter(x, y):
            px = x * scale
            py = (maze_height - y - 1) * scale  # Flip Y-axis
            return px, py

        # Draw vertical lines
        for x in range(maze_width):
            y = 0
            while y < maze_height:
                # If we find a wall cell
                if self.grid[y][x] == 1:
                    # Start of the wall line
                    start_y = y
                    # Find the end of the wall line
                    while y < maze_height and self.grid[y][x] == 1:
                        y += 1
                    end_y = y - 1
                    # Generate G-code for the line
                    x0, y0 = grid_to_plotter(x, start_y)
                    x1, y1 = grid_to_plotter(x, end_y)
                    gcode_commands.append(f'G0 X{x0:.2f} Y{y0:.2f}')  # Pen up move
                    gcode_commands.append('G1 Z-1 F500')  # Pen down
                    gcode_commands.append(f'G1 X{x1:.2f} Y{y1:.2f} F2500')  # Draw line
                    gcode_commands.append('G0 Z3')  # Pen up
                else:
                    y += 1

        # Draw horizontal lines
        for y in range(maze_height):
            x = 0
            while x < maze_width:
                # If we find a wall cell
                if self.grid[y][x] == 1:
                    # Start of the wall line
                    start_x = x
                    # Find the end of the wall line
                    while x < maze_width and self.grid[y][x] == 1:
                        x += 1
                    end_x = x - 1
                    # Generate G-code for the line
                    x0, y0 = grid_to_plotter(start_x, y)
                    x1, y1 = grid_to_plotter(end_x, y)
                    gcode_commands.append(f'G0 X{x0:.2f} Y{y0:.2f}')  # Pen up move
                    gcode_commands.append('G1 Z-1 F500')  # Pen down
                    gcode_commands.append(f'G1 X{x1:.2f} Y{y1:.2f} F2500')  # Draw line
                    gcode_commands.append('G0 Z3')  # Pen up
                else:
                    x += 1

        # Optionally, draw the solution path
        if include_solution:
            solution = self.find_path()
            if solution:
                # Move to the start of the solution path
                x0, y0 = grid_to_plotter(solution[0][1] * 2 + 1, solution[0][0] * 2 + 1)
                gcode_commands.append(f'G0 X{x0:.2f} Y{y0:.2f}')  # Move to start
                gcode_commands.append('G1 Z-1 F500')  # Pen down
                for y, x in solution[1:]:
                    x1, y1 = grid_to_plotter(x * 2 + 1, y * 2 + 1)
                    gcode_commands.append(f'G1 X{x1:.2f} Y{y1:.2f} F2500')  # Draw line
                gcode_commands.append('G0 Z3')  # Pen up

        # Return the G-code commands
        return '\n'.join(gcode_commands)



    def find_path(self):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        def get_neighbors(row, col):
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]) and self.grid[nr][nc] == 0:
                    yield (nr, nc)

        start, goal = self.start, self.finish

        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next in get_neighbors(*current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        # Reconstruct path
        path = []
        current = goal
        while current and current != start:
            path.append(current)
            current = came_from.get(current)
        
        if current != start:
            return None
        
        path.append(start)
        path.reverse()
        return path

    def calculate_difficulty(self):
        path = self.find_path()
        path_length = len(path) if path else 0

        # Total number of cells (excluding walls)
        total_cells = self.width * self.height

        # Calculate path difficulty: longer paths in larger mazes should be more difficult
        path_difficulty = path_length / (2 * total_cells - 1) if total_cells > 0 else 0

        # Initialize counters
        dead_ends = 0
        intersections = 0
        total_open_cells = 0
        total_branches = 0

        for y in range(self.height):
            for x in range(self.width):
                cell_y, cell_x = y * 2 + 1, x * 2 + 1
                if self.grid[cell_y][cell_x] == 0:
                    total_open_cells += 1
                    # Count open neighbors
                    open_neighbors = 0
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            neighbor_cell_y, neighbor_cell_x = ny * 2 + 1, nx * 2 + 1
                            if self.grid[neighbor_cell_y][neighbor_cell_x] == 0:
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
        wall_cells = sum(1 for row in self.grid for cell in row if cell == 1)
        possible_walls = len(self.grid) * len(self.grid[0])
        density = wall_cells / possible_walls

        # Combine metrics into a difficulty score
        difficulty = (
            0.55 * path_difficulty +         # Emphasize path length
            0.25 * dead_end_fraction +       # Dead ends contribute to difficulty
            0.20 * intersection_fraction +   # Intersections increase complexity
            0.20 * average_branching_factor  # More choices increase difficulty
        )

        return difficulty
