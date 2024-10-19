import random
from disjoint_set import DisjointSet

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
