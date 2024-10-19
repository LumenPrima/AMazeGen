import random

def generate_hunt_and_kill(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    visited = [[False] * width for _ in range(height)]

    def neighbors(x, y):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(x + dx, y + dy) for dx, dy in dirs if 0 <= x + dx < width and 0 <= y + dy < height]

    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    visited[y][x] = True
    grid[y * 2 + 1][x * 2 + 1] = 0

    while True:
        unvisited_neighbors = [(nx, ny) for nx, ny in neighbors(x, y) if not visited[ny][nx]]
        if unvisited_neighbors:
            # Randomly select an unvisited neighbor
            nx, ny = random.choice(unvisited_neighbors)
            # Remove wall between cells
            wall_x = x * 2 + 1 + (nx - x)
            wall_y = y * 2 + 1 + (ny - y)
            grid[wall_y][wall_x] = 0
            grid[ny * 2 + 1][nx * 2 + 1] = 0
            visited[ny][nx] = True
            x, y = nx, ny
        else:
            # Hunt for the next unvisited cell
            found = False
            for j in range(height):
                for i in range(width):
                    if not visited[j][i]:
                        adjacents = [(nx, ny) for nx, ny in neighbors(i, j) if visited[ny][nx]]
                        if adjacents:
                            # Remove wall between cells
                            nx, ny = random.choice(adjacents)
                            wall_x = i * 2 + 1 + (nx - i)
                            wall_y = j * 2 + 1 + (ny - j)
                            grid[wall_y][wall_x] = 0
                            grid[j * 2 + 1][i * 2 + 1] = 0
                            visited[j][i] = True
                            x, y = i, j
                            found = True
                            break
                if found:
                    break
            if not found:
                break  # Maze is complete
