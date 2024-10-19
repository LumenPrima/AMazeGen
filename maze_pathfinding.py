import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(maze, row, col):
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < len(maze.grid) and 0 <= nc < len(maze.grid[0]) and maze.grid[nr][nc] == 0:
            yield (nr, nc)

def find_path(maze):
    start, goal = maze.start, maze.finish

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == goal:
            break

        for next in get_neighbors(maze, *current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    # Reconstruct path
    path = []
    current = goal
    while current and current != start:
        path.append(current)
        current = came_from.get(current)
    
    if current != start:
        return None
    
    path.append(start)
    path.reverse()
    return path
