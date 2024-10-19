import random

def generate_recursive_backtracker(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    visited = [[False] * width for _ in range(height)]

    def carve(x, y):
        visited[y][x] = True
        grid[y * 2 + 1][x * 2 + 1] = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
                carve(nx, ny)

    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    carve(x, y)
