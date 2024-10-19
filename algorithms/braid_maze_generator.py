import random

def generate_braid_maze_generator(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    # First, generate a perfect maze using a simple algorithm like Binary Tree
    for y in range(height):
        for x in range(width):
            # Initialize all cells as walls
            grid[y * 2 + 1][x * 2 + 1] = 0
            
            # Carve passages
            if y < height - 1 and (x == width - 1 or random.choice([True, False])):
                grid[y * 2 + 2][x * 2 + 1] = 0  # Carve south
            elif x < width - 1:
                grid[y * 2 + 1][x * 2 + 2] = 0  # Carve east

    # Now, remove all dead ends to create a braid maze
    for y in range(height):
        for x in range(width):
            cell_y, cell_x = y * 2 + 1, x * 2 + 1
            
            # Count the number of walls around the cell
            walls = sum([
                grid[cell_y - 1][cell_x],  # North
                grid[cell_y + 1][cell_x],  # South
                grid[cell_y][cell_x - 1],  # West
                grid[cell_y][cell_x + 1]   # East
            ])
            
            # If the cell has 3 walls (dead end), remove one randomly
            if walls == 3:
                while True:
                    direction = random.choice(["N", "S", "W", "E"])
                    if direction == "N" and cell_y > 1 and grid[cell_y - 1][cell_x] == 1:
                        grid[cell_y - 1][cell_x] = 0
                        break
                    elif direction == "S" and cell_y < height * 2 - 1 and grid[cell_y + 1][cell_x] == 1:
                        grid[cell_y + 1][cell_x] = 0
                        break
                    elif direction == "W" and cell_x > 1 and grid[cell_y][cell_x - 1] == 1:
                        grid[cell_y][cell_x - 1] = 0
                        break
                    elif direction == "E" and cell_x < width * 2 - 1 and grid[cell_y][cell_x + 1] == 1:
                        grid[cell_y][cell_x + 1] = 0
                        break

    # Ensure outer walls are intact
    for x in range(width * 2 + 1):
        grid[0][x] = 1
        grid[height * 2][x] = 1
    for y in range(height * 2 + 1):
        grid[y][0] = 1
        grid[y][width * 2] = 1
