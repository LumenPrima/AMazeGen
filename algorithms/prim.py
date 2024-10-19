import random
from collections import deque

def generate_prim(maze):
    start = (random.randint(0, maze.width - 1), random.randint(0, maze.height - 1))
    maze.grid[start[1] * 2 + 1][start[0] * 2 + 1] = 0
    walls = deque([(start[0], start[1], dx, dy) for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                   if 0 <= start[0] + dx < maze.width and 0 <= start[1] + dy < maze.height])
    
    while walls:
        x, y, dx, dy = walls.popleft()
        nx, ny = x + dx, y + dy
        if 0 <= nx < maze.width and 0 <= ny < maze.height and maze.grid[ny * 2 + 1][nx * 2 + 1] == 1:
            maze.grid[ny * 2 + 1][nx * 2 + 1] = maze.grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
            for ndx, ndy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if 0 <= nx + ndx < maze.width and 0 <= ny + ndy < maze.height:
                    walls.append((nx, ny, ndx, ndy))
            random.shuffle(walls)
