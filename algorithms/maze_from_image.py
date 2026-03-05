from collections import deque
from PIL import Image

def generate_maze_from_image(maze, image_path=None):
    if image_path is None:
        raise ValueError("image_path is required for maze_from_image algorithm")

    img = Image.open(image_path).convert('L')  # Convert to grayscale
    grid_w = maze.width * 2 + 1
    grid_h = maze.height * 2 + 1
    img = img.resize((grid_w, grid_h))
    grid = maze.grid

    for y in range(grid_h):
        for x in range(grid_w):
            pixel = img.getpixel((x, y))
            grid[y][x] = 0 if pixel > 128 else 1  # Threshold at 128

    # Enforce border walls
    for x in range(grid_w):
        grid[0][x] = 1
        grid[grid_h - 1][x] = 1
    for y in range(grid_h):
        grid[y][0] = 1
        grid[y][grid_w - 1] = 1

    # Set start and finish explicitly
    grid[1][1] = 0
    grid[grid_h - 2][grid_w - 2] = 0
    maze.start = (1, 1)
    maze.finish = (grid_h - 2, grid_w - 2)

    # Ensure connectivity so the maze is solvable
    _ensure_connectivity(grid, grid_w, grid_h)


def _ensure_connectivity(grid, width, height):
    """Flood-fill from (1,1) and connect any isolated open regions."""
    visited = [[False] * width for _ in range(height)]
    queue = deque([(1, 1)])
    visited[1][1] = True

    while queue:
        y, x = queue.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 < ny < height - 1 and 0 < nx < width - 1 and not visited[ny][nx] and grid[ny][nx] == 0:
                visited[ny][nx] = True
                queue.append((ny, nx))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if grid[y][x] == 0 and not visited[y][x]:
                _connect_to_main(grid, visited, y, x, width, height)


def _connect_to_main(grid, visited, start_y, start_x, width, height):
    """Carve a path from an isolated cell to the main connected component."""
    queue = deque([(start_y, start_x, [(start_y, start_x)])])
    seen = {(start_y, start_x)}

    while queue:
        y, x, path = queue.popleft()
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 < ny < height - 1 and 0 < nx < width - 1 and (ny, nx) not in seen:
                if visited[ny][nx]:
                    for py, px in path:
                        grid[py][px] = 0
                        visited[py][px] = True
                    return
                seen.add((ny, nx))
                queue.append((ny, nx, path + [(ny, nx)]))
