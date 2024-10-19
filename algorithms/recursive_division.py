import random
import sys
from maze_utils import select_start_finish  # Import the function

# Increase the recursion limit
sys.setrecursionlimit(10000)

def generate_recursive_division(maze):
    width, height = maze.width * 2 + 1, maze.height * 2 + 1
    grid = [[0 for _ in range(width)] for _ in range(height)]

    def divide(x, y, w, h, orientation, depth=0):
        if depth > 1000:  # Set a maximum recursion depth
            return
        if w < 5 or h < 5:  # Base case for small areas
            for i in range(y, y + h, 2):
                for j in range(x, x + w, 2):
                    grid[i][j] = 0
            return

        horizontal = orientation if orientation is not None else random.choice([True, False])

        if horizontal:
            wy = y + random.randrange(1, h - 1, 2)
            px = x + random.randrange(0, w, 2)
            for i in range(x, x + w):
                if i != px:
                    grid[wy][i] = 1
            divide(x, y, w, wy - y + 1, None, depth + 1)
            divide(x, wy + 1, w, y + h - wy - 1, None, depth + 1)
        else:
            wx = x + random.randrange(1, w - 1, 2)
            py = y + random.randrange(0, h, 2)
            for i in range(y, y + h):
                if i != py:
                    grid[i][wx] = 1
            divide(x, y, wx - x + 1, h, None, depth + 1)
            divide(wx + 1, y, x + w - wx - 1, h, None, depth + 1)

    divide(1, 1, width - 2, height - 2, None)

    # Add border walls
    for y in range(height):
        grid[y][0] = grid[y][width - 1] = 1
    for x in range(width):
        grid[0][x] = grid[height - 1][x] = 1

    # Ensure start and finish are open
    select_start_finish(maze)  # Use the imported function instead of calling it as a method
    start_y, start_x = maze.start
    finish_y, finish_x = maze.finish
    grid[start_y][start_x] = 0
    grid[finish_y][finish_x] = 0

    # Connect isolated areas
    def connect_isolated_areas():
        visited = [[False for _ in range(width)] for _ in range(height)]
        
        def flood_fill(y, x):
            if not (0 <= y < height and 0 <= x < width) or visited[y][x] or grid[y][x] == 1:
                return
            visited[y][x] = True
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                flood_fill(y + dy, x + dx)

        flood_fill(start_y, start_x)

        for y in range(1, height - 1, 2):
            for x in range(1, width - 1, 2):
                if grid[y][x] == 0 and not visited[y][x]:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    random.shuffle(directions)
                    for dy, dx in directions:
                        ny, nx = y + dy, x + dx
                        if visited[ny][nx]:
                            grid[y + dy // 2][x + dx // 2] = 0
                            flood_fill(y, x)
                            break

    connect_isolated_areas()

    # Copy the generated maze directly to the maze object
    for y in range(height):
        for x in range(width):
            maze.grid[y][x] = grid[y][x]

    # Ensure the maze is valid
    verify_maze(maze)

def verify_maze(maze):
    width, height = maze.width * 2 + 1, maze.height * 2 + 1
    visited = [[False for _ in range(width)] for _ in range(height)]
    stack = [maze.start]

    while stack:
        y, x = stack.pop()
        if not visited[y][x]:
            visited[y][x] = True
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < height and 0 <= nx < width and maze.grid[ny][nx] == 0 and not visited[ny][nx]:
                    stack.append((ny, nx))

    # Check if all open cells are connected
    for y in range(height):
        for x in range(width):
            if maze.grid[y][x] == 0 and not visited[y][x]:
                raise ValueError("Invalid maze: not all open cells are connected")

    # Check if start and finish are connected
    if not visited[maze.finish[0]][maze.finish[1]]:
        raise ValueError("Invalid maze: start and finish are not connected")

    print("Maze verification passed")
