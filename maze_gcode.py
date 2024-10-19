def to_gcode(maze, cell_size=10, margin=10, max_size=200, include_solution=False):
    maze_width = (maze.width * 2 + 1)
    maze_height = (maze.height * 2 + 1)
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
            if maze.grid[y][x] == 1:
                # Start of the wall line
                start_y = y
                # Find the end of the wall line
                while y < maze_height and maze.grid[y][x] == 1:
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
            if maze.grid[y][x] == 1:
                # Start of the wall line
                start_x = x
                # Find the end of the wall line
                while x < maze_width and maze.grid[y][x] == 1:
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
        solution = maze.find_path()
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
