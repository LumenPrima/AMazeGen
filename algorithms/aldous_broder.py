import random

def generate_aldous_broder(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    visited = [[False] * width for _ in range(height)]

    # Start at a random cell
    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    visited_cells = 1
    total_cells = width * height
    visited[y][x] = True
    grid[y * 2 + 1][x * 2 + 1] = 0

    while visited_cells < total_cells:
        # Choose a random neighbor
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        dx, dy = directions[0]
        nx, ny = x + dx, y + dy

        if 0 <= nx < width and 0 <= ny < height:
            if not visited[ny][nx]:
                # Carve passage between cells
                grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
                grid[ny * 2 + 1][nx * 2 + 1] = 0
                visited[ny][nx] = True
                visited_cells += 1
            x, y = nx, ny
