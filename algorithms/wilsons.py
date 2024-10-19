import random

def generate_wilsons(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    total_cells = width * height
    unvisited = {(x, y) for x in range(width) for y in range(height)}
    in_maze = set()

    # Start with a random cell
    first_cell = random.choice(list(unvisited))
    unvisited.remove(first_cell)
    in_maze.add(first_cell)
    grid[first_cell[1] * 2 + 1][first_cell[0] * 2 + 1] = 0

    while unvisited:
        # Choose a random unvisited cell
        cell = random.choice(list(unvisited))
        path = [cell]

        while cell not in in_maze:
            # Randomly walk to a neighbor
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            dx, dy = random.choice(directions)
            nx, ny = cell[0] + dx, cell[1] + dy

            if 0 <= nx < width and 0 <= ny < height:
                cell = (nx, ny)
                if cell in path:
                    # Loop detected; erase the loop
                    loop_index = path.index(cell)
                    path = path[:loop_index + 1]
                else:
                    path.append(cell)
        # Add the path to the maze
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            grid[y1 * 2 + 1][x1 * 2 + 1] = 0
            grid[(y1 + y2) + 1][(x1 + x2) + 1] = 0
            unvisited.discard((x1, y1))
            in_maze.add((x1, y1))
        unvisited.discard(path[-1])
        in_maze.add(path[-1])
        grid[path[-1][1] * 2 + 1][path[-1][0] * 2 + 1] = 0
