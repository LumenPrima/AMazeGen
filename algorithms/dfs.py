import random

def generate_dfs(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    # Starting position (random or fixed)
    start_x, start_y = random.randint(0, width - 1), random.randint(0, height - 1)

    # Initialize the stack with the starting cell
    stack = [(start_x, start_y)]
    visited = [[False] * width for _ in range(height)]
    visited[start_y][start_x] = True

    while stack:
        x, y = stack[-1]
        # List of possible directions (left, right, up, down)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        found = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check boundaries and if the neighbor is unvisited
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                # Remove the wall between the current cell and the neighbor
                wall_x = x * 2 + 1 + dx
                wall_y = y * 2 + 1 + dy
                grid[wall_y][wall_x] = 0
                # Remove the wall of the neighbor cell
                cell_x = nx * 2 + 1
                cell_y = ny * 2 + 1
                grid[cell_y][cell_x] = 0
                # Mark the neighbor as visited and push it onto the stack
                visited[ny][nx] = True
                stack.append((nx, ny))
                found = True
                break  # Move to the next cell

        if not found:
            # Backtrack if no unvisited neighbors
            stack.pop()
