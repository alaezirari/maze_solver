import time
import tracemalloc
from collections import deque
import heapq


# heuristique (manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# definir les distances possibles haut,bas, gauche, droite
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# fonctions pour obtenir les voisins valides
def get_neighbors(node, maze):
    x, y = node
    return [
        (x + dx, y + dy)
        for dx, dy in directions
        if (x + dx, y + dy) in maze and maze[(x + dx, y + dy)] == 0
    ]


# A* algorithm
def a_star(start, goal, maze, heuristic):
    metrics = {"time": [], "memory": []}
    tracemalloc.start()
    start_time = time.time()

    open_set = []
    heapq.heappush(
        open_set, (0 + heuristic(start, goal), start)
    )  # ajout de l'heuristique au coût initial
    came_from = {start: None}
    g_score = {start: 0}
    while open_set:
        _, current = heapq.heappop(open_set)
        metrics["time"].append(time.time() - start_time)
        metrics["memory"].append(tracemalloc.get_traced_memory()[1] / 1024)  # en KB
        if current == goal:
            break
    for neighbor in get_neighbors(current, maze):
        tentative_g_score = g_score[current] + 1
        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score = tentative_g_score + heuristic(neighbor, goal)
            heapq.heappush(open_set, (f_score, neighbor))
    tracemalloc.stop()
    path = []
    while current:
        path.append(current)
        current = came_from[current]
    return path[::-1], metrics


# gbfs algorithm
def gbfs(start, goal, maze, heuristic):
    metrics = {"time": [], "memory": []}
    tracemalloc.start()
    start_time = time.time()

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}
    while open_set:
        _, current = heapq.heappop(open_set)
        metrics["time"].append(time.time() - start_time)
        metrics["memory"].append(tracemalloc.get_traced_memory()[1] / 1024)
        if current == goal:
            break
        for neighbor in get_neighbors(current, maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                priority = heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, neighbor))
    tracemalloc.stop()
    path = []
    current = goal  # pour reconstruire le chemin à partir du goal
    while current:
        path.append(current)
        current = came_from[current]
    return path[::-1], metrics


# bfs algorithm
def bfs(start, goal, maze):
    metrics = {"time": [], "memory": []}
    tracemalloc.start()  ###
    start_time = time.time()  ###
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()

        ### a ce niveau on registre le temps et la mémoire consommes
        metrics["time"].append(time.time() - start_time)
        metrics["memory"].append(tracemalloc.get_traced_memory()[1] / 1024)  # en KB
        ###

        if current == goal:
            break
        for neighbor in get_neighbors(current, maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)
    tracemalloc.stop()  ###
    path = []
    current = goal  # pour reconstruire le chemin à partir du goal
    while current:
        path.append(current)
        current = came_from[current]
    return path[::-1], metrics


# dfs algorithm
def dfs(start, goal, maze):
    metrics = {"time": [], "memory": []}
    tracemalloc.start()  ###
    start_time = time.time()  ###
    stack = [start]
    came_from = {start: None}
    while stack:
        current = stack.pop()
        metrics["time"].append(time.time() - start_time)
        metrics["memory"].append(tracemalloc.get_traced_memory()[1] / 1024)
        if current == goal:
            break
        for neighbor in get_neighbors(current, maze):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)
    tracemalloc.stop()
    path = []
    current = goal
    while current:
        path.append(current)
        current = came_from[current]
    return path[::-1], metrics
