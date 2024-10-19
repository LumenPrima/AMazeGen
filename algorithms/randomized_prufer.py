import random

def generate_randomized_prufer(maze):
    width, height = maze.width, maze.height
    grid = maze.grid

    def get_cell_index(x, y):
        return y * width + x

    def get_cell_coords(index):
        return index % width, index // width

    # Generate a random Prüfer sequence
    sequence_length = width * height - 2
    prufer_sequence = [random.randint(0, width * height - 1) for _ in range(sequence_length)]

    # Count the occurrences of each vertex in the Prüfer sequence
    vertex_counts = [0] * (width * height)
    for vertex in prufer_sequence:
        vertex_counts[vertex] += 1

    # Construct the tree from the Prüfer sequence
    edges = []
    for i in range(sequence_length):
        for j in range(width * height):
            if vertex_counts[j] == 0:
                edges.append((j, prufer_sequence[i]))
                vertex_counts[j] = -1
                vertex_counts[prufer_sequence[i]] -= 1
                break

    # Add the last edge
    last_vertices = [i for i in range(width * height) if vertex_counts[i] == 0]
    edges.append((last_vertices[0], last_vertices[1]))

    # Carve passages based on the edges
    for edge in edges:
        x1, y1 = get_cell_coords(edge[0])
        x2, y2 = get_cell_coords(edge[1])
        
        # Ensure we're not carving through the outer walls
        if 0 < x1 < width-1 and 0 < y1 < height-1 and 0 < x2 < width-1 and 0 < y2 < height-1:
            mid_x = x1 + (x2 - x1) // 2
            mid_y = y1 + (y2 - y1) // 2
            grid[y1 * 2 + 1][x1 * 2 + 1] = 0  # Mark cell as passage
            grid[y2 * 2 + 1][x2 * 2 + 1] = 0  # Mark cell as passage
            grid[mid_y * 2 + 1][mid_x * 2 + 1] = 0  # Mark the wall between cells as passage

    # Ensure outer walls are intact
    for x in range(width * 2 + 1):
        grid[0][x] = 1
        grid[height * 2][x] = 1
    for y in range(height * 2 + 1):
        grid[y][0] = 1
        grid[y][width * 2] = 1
