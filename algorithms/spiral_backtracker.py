import random

def generate_spiral_backtracker(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    # Starting position (center of the maze)
    start_x, start_y = width // 2, height // 2

    # Initialize the stack with the starting cell
    stack = [(start_x, start_y)]
    visited = [[False] * width for _ in range(height)]
    visited[start_y][start_x] = True

    # Spiral directions: right, down, left, up
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction_index = 0

    while stack:
        x, y = stack[-1]
        
        # Try to move in the current spiral direction
        dx, dy = directions[direction_index]
        nx, ny = x + dx, y + dy

        # Check if we can move in the current direction
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
        else:
            # If we can't move in the current direction, try the next direction
            direction_index = (direction_index + 1) % 4
            
            # If we've tried all directions, backtrack
            if direction_index == 0:
                stack.pop()

                # Occasionally create a loop to make the maze more interesting
                if random.random() < 0.1 and len(stack) > 1:
                    prev_x, prev_y = stack[-1]
                    for dx, dy in directions:
                        loop_x, loop_y = prev_x + dx, prev_y + dy
                        if 0 <= loop_x < width and 0 <= loop_y < height and visited[loop_y][loop_x] and (loop_x, loop_y) != (x, y):
                            wall_x = prev_x * 2 + 1 + dx
                            wall_y = prev_y * 2 + 1 + dy
                            grid[wall_y][wall_x] = 0
                            break
