import random
from disjoint_set import DisjointSet
from collections import deque

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


def generate_kruskal(maze):
    edges = [(x, y, dx, dy) for x in range(maze.width) for y in range(maze.height)
             for dx, dy in [(1, 0), (0, 1)] if x + dx < maze.width and y + dy < maze.height]
    random.shuffle(edges)
    ds = DisjointSet([(x, y) for x in range(maze.width) for y in range(maze.height)])
    
    for x, y, dx, dy in edges:
        if ds.find((x, y)) != ds.find((x + dx, y + dy)):
            ds.union((x, y), (x + dx, y + dy))
            maze.grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
            maze.grid[y * 2 + 1][x * 2 + 1] = maze.grid[(y + dy) * 2 + 1][(x + dx) * 2 + 1] = 0

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

def generate_recursive_division(maze):
    width, height = maze.width * 2 + 1, maze.height * 2 + 1
    grid = maze.grid

    def divide(x, y, w, h, orientation):
        if w < 3 or h < 3:
            return

        horizontal = orientation == 'H'

        # Where will the wall be drawn?
        wx = x + (0 if horizontal else random.randrange(0, w // 2) * 2 + 1)
        wy = y + (random.randrange(0, h // 2) * 2 + 1 if horizontal else 0)

        # Where will the passage through the wall exist?
        px = wx + (random.randrange(0, w // 2) * 2 + 1 if horizontal else 0)
        py = wy + (0 if horizontal else random.randrange(0, h // 2) * 2 + 1)

        # Direction of wall
        dx = 1 if horizontal else 0
        dy = 0 if horizontal else 1

        # Length of wall
        length = w if horizontal else h
        length = length // 2 * 2

        # Draw the wall
        for i in range(length):
            if (wx != px or wy != py):
                grid[wy][wx] = 1
            wx += dx
            wy += dy

        # Recursively divide the subareas
        nx, ny = x, y
        nw, nh = (w, wy - y) if horizontal else (wx - x, h)
        divide(nx, ny, nw, nh, choose_orientation(nw, nh))

        nx, ny = (x, wy + 1) if horizontal else (wx + 1, y)
        nw, nh = (w, y + h - wy - 1) if horizontal else (x + w - wx - 1, h)
        divide(nx, ny, nw, nh, choose_orientation(nw, nh))

    def choose_orientation(w, h):
        if w < h:
            return 'H'
        elif h < w:
            return 'V'
        else:
            return 'H' if random.choice([True, False]) else 'V'

    # Initialize the grid with walls
    for y in range(height):
        for x in range(width):
            grid[y][x] = 1

    # Carve out the initial area
    for y in range(1, height, 2):
        for x in range(1, width, 2):
            grid[y][x] = 0

    # Start the division
    divide(1, 1, width - 2, height - 2, choose_orientation(width, height))

def generate_recursive_division(maze):
    width, height = maze.width * 2 + 1, maze.height * 2 + 1
    grid = maze.grid

    def divide(x, y, w, h, orientation):
        if w <= 2 or h <= 2:
            return

        horizontal = orientation == 'H'

        # Possible wall positions
        if horizontal:
            possible_walls = [y + i for i in range(2, h, 2)]
            possible_passages = [x + i for i in range(1, w, 2)]
        else:
            possible_walls = [x + i for i in range(2, w, 2)]
            possible_passages = [y + i for i in range(1, h, 2)]

        # Return if not enough space to divide further
        if not possible_walls or not possible_passages:
            return

        # Where will the wall be drawn?
        wall_pos = random.choice(possible_walls)

        # Where will the passage through the wall exist?
        passage_pos = random.choice(possible_passages)

        # Draw the wall
        if horizontal:
            for i in range(x, x + w):
                if i != passage_pos and 0 <= wall_pos < height and 0 <= i < width:
                    grid[wall_pos][i] = 1
        else:
            for i in range(y, y + h):
                if i != passage_pos and 0 <= i < height and 0 <= wall_pos < width:
                    grid[i][wall_pos] = 1

        # Recursively divide the subareas
        if horizontal:
            divide(x, y, w, wall_pos - y, choose_orientation(w, wall_pos - y))
            divide(x, wall_pos + 1, w, y + h - wall_pos - 1, choose_orientation(w, y + h - wall_pos - 1))
        else:
            divide(x, y, wall_pos - x, h, choose_orientation(wall_pos - x, h))
            divide(wall_pos + 1, y, x + w - wall_pos - 1, h, choose_orientation(x + w - wall_pos - 1, h))

    def choose_orientation(w, h):
        if w < h:
            return 'H'
        elif h < w:
            return 'V'
        else:
            return 'H' if random.choice([True, False]) else 'V'

    # Initialize the grid with walls
    for y in range(height):
        for x in range(width):
            grid[y][x] = 1

    # Carve out the initial area
    for y in range(1, height, 2):
        for x in range(1, width, 2):
            grid[y][x] = 0

    # Start the division
    divide(1, 1, width - 2, height - 2, choose_orientation(width - 2, height - 2))


def generate_aldous_broder(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    # Start at a random cell
    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    total_cells = width * height
    visited_cells = 1

    # Mark the starting cell as open
    grid[y * 2 + 1][x * 2 + 1] = 0

    while visited_cells < total_cells:
        # Choose a random neighbor
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dx, dy = random.choice(directions)
        nx, ny = x + dx, y + dy

        if 0 <= nx < width and 0 <= ny < height:
            if grid[ny * 2 + 1][nx * 2 + 1] == 1:
                # Carve passage between cells
                grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
                grid[ny * 2 + 1][nx * 2 + 1] = 0
                visited_cells += 1
            x, y = nx, ny
        else:
            # Move to the neighbor even if it's visited
            x, y = nx, ny

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

def generate_ellers(maze):
    width, height = maze.width, maze.height
    grid = maze.grid
    sets = [{} for _ in range(height)]
    next_set = 1

    for y in range(height):
        # Assign sets to cells
        for x in range(width):
            if grid[y * 2 + 1][x * 2 + 1] == 1:
                grid[y * 2 + 1][x * 2 + 1] = 0
                sets[y][x] = next_set
                next_set += 1

        # Merge adjacent cells horizontally
        for x in range(width - 1):
            if random.choice([True, False]) or sets[y][x] == sets[y][x + 1]:
                continue
            grid[y * 2 + 1][x * 2 + 2] = 0  # Remove right wall
            old_set = sets[y][x + 1]
            for k in range(width):
                if sets[y][k] == old_set:
                    sets[y][k] = sets[y][x]

        # Prepare for vertical connections
        if y < height - 1:
            # Decide which cells will connect downward
            set_cells = {}
            for x in range(width):
                cell_set = sets[y][x]
                set_cells.setdefault(cell_set, []).append(x)
            for cell_set, cells in set_cells.items():
                connect_down = random.sample(cells, random.randint(1, len(cells)))
                for x in cells:
                    if x in connect_down:
                        grid[y * 2 + 2][x * 2 + 1] = 0  # Remove bottom wall
                        sets[y + 1][x] = cell_set  # Carry set down
                    else:
                        sets[y + 1][x] = None
        else:
            # Last row: ensure all cells are connected
            for x in range(width - 1):
                if sets[y][x] != sets[y][x + 1]:
                    grid[y * 2 + 1][x * 2 + 2] = 0  # Remove right wall
                    old_set = sets[y][x + 1]
                    for k in range(width):
                        if sets[y][k] == old_set:
                            sets[y][k] = sets[y][x]

def generate_sidewinder(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    for y in range(height):
        run = []
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0
            run.append((x, y))
            carve_east = random.choice([True, False]) if y > 0 else True

            if x == width - 1 or not carve_east:
                # Carve north in the run
                cell_x, cell_y = random.choice(run)
                if cell_y > 0:
                    grid[cell_y * 2][cell_x * 2 + 1] = 0  # Remove north wall
                run = []
            else:
                # Carve east
                grid[y * 2 + 1][x * 2 + 2] = 0  # Remove east wall

def generate_binary_tree(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    for y in range(height):
        for x in range(width):
            grid[y * 2 + 1][x * 2 + 1] = 0
            directions = []
            if x < width - 1:
                directions.append((1, 0))  # East
            if y > 0:
                directions.append((0, -1))  # North
            if directions:
                dx, dy = random.choice(directions)
                nx, ny = x + dx, y + dy
                grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0

def generate_growing_tree(maze, selection_method='random'):
    width, height = maze.width, maze.height
    grid = maze.grid

    x, y = random.randint(0, width - 1), random.randint(0, height - 1)
    grid[y * 2 + 1][x * 2 + 1] = 0
    cells = [(x, y)]

    while cells:
        if selection_method == 'newest':
            index = -1
        elif selection_method == 'random':
            index = random.randint(0, len(cells) - 1)
        elif selection_method == 'oldest':
            index = 0
        else:
            index = -1  # Default to newest

        x, y = cells[index]
        directions = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny * 2 + 1][nx * 2 + 1] == 1:
                directions.append((dx, dy))

        if directions:
            dx, dy = random.choice(directions)
            nx, ny = x + dx, y + dy
            # Remove wall between cells
            grid[y * 2 + 1 + dy][x * 2 + 1 + dx] = 0
            grid[ny * 2 + 1][nx * 2 + 1] = 0
            cells.append((nx, ny))
        else:
            cells.pop(index)

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

def generate_cellular_automata(maze, generations=4):
    width, height = maze.width * 2 + 1, maze.height * 2 + 1
    grid = maze.grid

    # Initialize grid with random walls
    for y in range(height):
        for x in range(width):
            grid[y][x] = 1 if random.random() < 0.4 else 0

    # Apply cellular automata rules
    for _ in range(generations):
        new_grid = [row[:] for row in grid]
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                wall_count = sum(grid[ny][nx] for nx in range(x - 1, x + 2)
                                 for ny in range(y - 1, y + 2) if (nx, ny) != (x, y))
                if wall_count > 4:
                    new_grid[y][x] = 1
                elif wall_count < 4:
                    new_grid[y][x] = 0
        grid[:] = new_grid[:]

    # Ensure start and finish are open
    grid[1][1] = 0
    grid[height - 2][width - 2] = 0


def generate_maze_from_image(maze, image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((maze.width * 2 + 1, maze.height * 2 + 1))
    grid = maze.grid

    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            grid[y][x] = 0 if pixel > 128 else 1  # Threshold at 128

    # Ensure start and finish are open
    grid[1][1] = 0
    grid[img.height - 2][img.width - 2] = 0

def generate_kruskal_weighted(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    # Initialize disjoint sets
    ds = DisjointSet([(x, y) for x in range(width) for y in range(height)])

    # Create all possible edges with weights
    edges = []
    for x in range(width):
        for y in range(height):
            for dx, dy in [(1, 0), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx < width and ny < height:
                    weight = random.randint(1, 100)  # Assign a random weight
                    edges.append((weight, (x, y), (nx, ny)))

    # Sort edges by weight
    edges.sort()

    # Initialize grid with walls
    for y in range(height * 2 + 1):
        for x in range(width * 2 + 1):
            grid[y][x] = 1

    # Process edges
    for weight, (x1, y1), (x2, y2) in edges:
        if ds.find((x1, y1)) != ds.find((x2, y2)):
            ds.union((x1, y1), (x2, y2))
            wall_x = x1 * 2 + 1 + (x2 - x1)
            wall_y = y1 * 2 + 1 + (y2 - y1)
            grid[wall_y][wall_x] = 0
            grid[y1 * 2 + 1][x1 * 2 + 1] = 0
            grid[y2 * 2 + 1][x2 * 2 + 1] = 0

def generate_aldous_broder_optimized(maze):
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

