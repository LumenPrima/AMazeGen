import random

def generate_recursive_backtracker(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    visited = [[False] * width for _ in range(height)]

    # Iterative DFS to avoid RecursionError on large mazes
    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    visited[y][x] = True
    grid[y * 2 + 1][x * 2 + 1] = 0
    stack = [(x, y)]

    while stack:
        x, y = stack[-1]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        found = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
                grid[ny * 2 + 1][nx * 2 + 1] = 0
                visited[ny][nx] = True
                stack.append((nx, ny))
                found = True
                break

        if not found:
            stack.pop()
