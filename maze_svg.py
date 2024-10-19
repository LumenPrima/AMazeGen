def to_svg(maze, cell_size=10, margin=10):
    width = (maze.width * 2 + 1) * cell_size + 2 * margin
    height = (maze.height * 2 + 1) * cell_size + 2 * margin
    svg_elements = []

    # Start SVG
    svg_header = f'<svg width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
    svg_elements.append(svg_header)
    svg_elements.append('<rect width="100%" height="100%" fill="white"/>')

    # Draw maze walls
    for y in range(maze.height * 2 + 1):
        for x in range(maze.width * 2 + 1):
            if maze.grid[y][x] == 1:
                wx = margin + x * cell_size
                wy = margin + y * cell_size
                svg_elements.append(f'<rect x="{wx}" y="{wy}" width="{cell_size}" height="{cell_size}" fill="black"/>')

    # Draw start and finish points
    if maze.start:
        sy, sx = maze.start
        cx = margin + sx * cell_size + cell_size // 2
        cy = margin + sy * cell_size + cell_size // 2
        svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{cell_size * 0.4}" fill="green"/>')

    if maze.finish:
        fy, fx = maze.finish
        cx = margin + fx * cell_size + cell_size // 2
        cy = margin + fy * cell_size + cell_size // 2
        svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="{cell_size * 0.4}" fill="red"/>')

    # End SVG
    svg_elements.append('</svg>')

    return '\n'.join(svg_elements)

def overlay_solution(maze, svg_content, cell_size=10, margin=10):
    # Extract the closing SVG tag to append solution before it
    svg_closing_tag = '</svg>'
    if svg_content.endswith(svg_closing_tag):
        svg_content = svg_content[:-len(svg_closing_tag)]
    else:
        # Handle the case where SVG might not end with '</svg>'
        pass

    # Draw solution path
    solution = maze.find_path()
    if solution and len(solution) > 1:  # Check if solution exists and has at least two points
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

def to_svg_with_solution(maze, cell_size=10, margin=10):
    # Generate the base maze SVG
    svg_base = to_svg(maze, cell_size, margin)

    # Overlay the solution path onto the base SVG
    svg_with_solution = overlay_solution(maze, svg_base, cell_size, margin)

    return svg_with_solution
