import pygame
import heapq
from collections import deque
import time

# --- CONFIGURATION ---
WIDTH, HEIGHT = 900, 600
GRID_SIZE = 20
COLS, ROWS = 30, 25
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)  # Start
GREEN = (50, 255, 50)  # End
BLUE = (50, 150, 255)  # Exploring
YELLOW = (255, 255, 0)  # Final Path
GREY = (200, 200, 200)  # Stats Text

# --- THE MAZE (A Hard Labyrinth) ---
# 1 = Wall, 0 = Path
MAZE_DATA = [
    [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        0,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        1,
    ],
    [
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        0,
        1,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        0,
        1,
    ],
    [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
    ],
    [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
    ],
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver Showdown: BFS vs DFS vs GBFS vs A*")
font = pygame.font.SysFont("monospace", 18)


def draw_maze(current_visited, path, stats, algo_name):
    screen.fill(BLACK)

    # Draw Grid
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE if MAZE_DATA[r][c] == 0 else BLACK
            if (r, c) == (1, 1):
                color = RED  # Start
            if (r, c) == (23, 28):
                color = GREEN  # End
            if (r, c) in current_visited:
                color = BLUE
            if (r, c) in path:
                color = YELLOW

            pygame.draw.rect(
                screen,
                color,
                (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1),
            )

    # Stats Panel
    pygame.draw.rect(screen, (40, 40, 40), (600, 0, 300, HEIGHT))
    title = font.render(f"ALGO: {algo_name}", True, YELLOW)
    s1 = font.render(f"Nodes Explored: {stats['nodes']}", True, WHITE)
    s2 = font.render(f"Path Length: {stats['path']}", True, WHITE)
    s3 = font.render(f"Memory (Max): {stats['mem']}", True, WHITE)

    screen.blit(title, (620, 50))
    screen.blit(s1, (620, 100))
    screen.blit(s2, (620, 140))
    screen.blit(s3, (620, 180))

    pygame.display.flip()


def get_solver(name):
    start, end = (1, 1), (23, 28)
    visited = set()
    stats = {"nodes": 0, "path": 0, "mem": 0}

    if name == "BFS":
        q = deque([(start, [])])
    elif name == "DFS":
        q = [(start, [])]
    elif name == "GBFS":
        q = [(0, start, [])]  # (h, pos, path)
    else:  # A*
        q = [(0, start, [])]  # (f, pos, path)

    while q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Logic per Algorithm
        if name == "BFS":
            curr, path = q.popleft()
        elif name == "DFS":
            curr, path = q.pop()
        else:
            _, curr, path = heapq.heappop(q)

        if curr == end:
            stats["path"] = len(path)
            draw_maze(visited, path + [end], stats, name)
            time.sleep(2)
            return

        if curr not in visited:
            visited.add(curr)
            stats["nodes"] += 1
            stats["mem"] = max(stats["mem"], len(q))

            r, c = curr
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE_DATA[nr][nc] == 0:
                    new_path = path + [curr]
                    if name == "BFS" or name == "DFS":
                        q.append(((nr, nc), new_path))
                    elif name == "GBFS":
                        h = abs(nr - end[0]) + abs(nc - end[1])
                        heapq.heappush(q, (h, (nr, nc), new_path))
                    else:  # A*
                        g = len(new_path)
                        h = abs(nr - end[0]) + abs(nc - end[1])
                        heapq.heappush(q, (g + h, (nr, nc), new_path))

        draw_maze(visited, path, stats, name)
        # pygame.time.delay(5) # Uncomment to slow it down


# Run the Showdown
for algo in ["BFS", "DFS", "GBFS", "ASTAR"]:
    get_solver(algo)

pygame.quit()
import pygame
import heapq
import matplotlib.pyplot as plt
from collections import deque
import time

# --- CONSTANTS ---
WIDTH, HEIGHT = 900, 600
GRID_SIZE = 15
COLS, ROWS = 40, 30
FPS = 120  # High FPS for faster project demo

# Colors
COLOR_MAP = {
    "wall": (30, 30, 35),
    "path": (255, 255, 255),
    "start": (0, 255, 0),
    "end": (255, 0, 0),
    "visited": (100, 150, 255, 100),  # Translucent blue
    "path_final": (255, 165, 0),  # Orange
    "text": (200, 200, 200),
}


# --- GENERATE A HARD CHALLENGE MAZE ---
# A "snake" pattern maze with traps
def create_maze():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # Outer walls
    for r in range(ROWS):
        grid[r][0] = grid[r][COLS - 1] = 1
    for c in range(COLS):
        grid[0][c] = grid[ROWS - 1][c] = 1

    # Complex Dividers (The "Snake" Labyrinth)
    for i in range(5, COLS - 5, 8):
        for j in range(0, ROWS - 8):
            grid[j][i] = 1
        for j in range(8, ROWS):
            grid[j][i + 4] = 1
    return grid


MAZE = create_maze()
START, END = (1, 1), (ROWS - 2, COLS - 2)

# --- STATS TRACKER ---
results_data = {
    "DFS": {"nodes": 0, "path": 0, "time": 0},
    "BFS": {"nodes": 0, "path": 0, "time": 0},
    "GBFS": {"nodes": 0, "path": 0, "time": 0},
    "ASTAR": {"nodes": 0, "path": 0, "time": 0},
}


def draw_interface(screen, visited, path, algo, nodes, font):
    screen.fill((20, 20, 25))
    # Draw Maze
    for r in range(ROWS):
        for c in range(COLS):
            rect = (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
            if MAZE[r][c] == 1:
                color = COLOR_MAP["wall"]
            elif (r, c) == START:
                color = COLOR_MAP["start"]
            elif (r, c) == END:
                color = COLOR_MAP["end"]
            elif (r, c) in path:
                color = COLOR_MAP["path_final"]
            elif (r, c) in visited:
                color = COLOR_MAP["visited"]
            else:
                color = (50, 50, 60)
            pygame.draw.rect(screen, color, rect)

    # UI Panel
    pygame.draw.rect(screen, (45, 45, 55), (600, 0, 300, HEIGHT))
    headers = [
        f"ALGORITHM: {algo}",
        f"Nodes Explored: {nodes}",
        f"Real-time Path: {len(path)}",
        "",
        "PROJECT LOGS:",
        "- BFS: Shortest Path guaranteed",
        "- DFS: Low memory, reckless",
        "- GBFS: Fast, ignores distance",
        "- A*: Optimal efficiency",
    ]
    for i, line in enumerate(headers):
        text = font.render(line, True, COLOR_MAP["text"])
        screen.blit(text, (620, 50 + (i * 30)))

    pygame.display.flip()


def run_solver(name, screen, font):
    start_time = time.time()
    visited = set()
    nodes_count = 0

    if name == "BFS":
        q = deque([(START, [])])
    elif name == "DFS":
        q = [(START, [])]
    else:
        q = [(0, START, [])]  # Priority Queue

    while q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if name == "BFS":
            curr, path = q.popleft()
        elif name == "DFS":
            curr, path = q.pop()
        else:
            _, curr, path = heapq.heappop(q)

        if curr == END:
            results_data[name] = {
                "nodes": nodes_count,
                "path": len(path),
                "time": round(time.time() - start_time, 4),
            }
            time.sleep(1)  # Pause to see result
            return

        if curr not in visited:
            visited.add(curr)
            nodes_count += 1
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
                    new_path = path + [curr]
                    if name in ["BFS", "DFS"]:
                        q.append(((nr, nc), new_path))
                    else:
                        h = abs(nr - END[0]) + abs(nc - END[1])
                        priority = h if name == "GBFS" else (len(new_path) + h)
                        heapq.heappush(q, (priority, (nr, nc), new_path))

        if nodes_count % 2 == 0:  # Speed up visualizer
            draw_interface(screen, visited, path, name, nodes_count, font)


# --- MAIN EXECUTION ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 18)

for algo in ["DFS", "BFS", "GBFS", "ASTAR"]:
    run_solver(algo, screen, font)
pygame.quit()


# --- ANALYTICS TAB (MATPLOTLIB) ---
def show_graphs():
    algos = list(results_data.keys())
    nodes = [results_data[a]["nodes"] for a in algos]
    paths = [results_data[a]["path"] for a in algos]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Maze Solver Project: Technical Comparison", fontsize=16)

    # Graph 1: Efficiency
    ax1.bar(algos, nodes, color=["salmon", "skyblue", "lightgreen", "gold"])
    ax1.set_title("Computational Effort (Nodes Explored)")
    ax1.set_ylabel("Lower is better")

    # Graph 2: Path Accuracy
    ax2.bar(algos, paths, color=["salmon", "skyblue", "lightgreen", "gold"])
    ax2.set_title("Path Quality (Steps to Exit)")
    ax2.set_ylabel("Lower is more direct")

    plt.tight_layout()
    plt.show()


show_graphs()
import pygame
import heapq
import matplotlib.pyplot as plt
from collections import deque
import time

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1000, 700
GRID_SIZE = 25
COLS, ROWS = 25, 20
TIME_DELAY = 0.05  # INCREASE THIS TO MAKE IT SLOWER (0.1 = 10 frames per second)

# Colors
COLOR_BG = (15, 15, 20)
COLOR_WALL = (40, 44, 52)
COLOR_PATH = (255, 255, 255)
COLOR_VISITED = (61, 139, 255)
COLOR_CURRENT = (255, 255, 0)  # The "Snake" head
COLOR_TEXT = (230, 230, 230)


# 1 = Wall, 0 = Empty
def get_hard_maze():
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # Create border
    for r in range(ROWS):
        grid[r][0] = grid[r][COLS - 1] = 1
    for c in range(COLS):
        grid[0][c] = grid[ROWS - 1][c] = 1

    # Add manual "trap" walls
    for r in range(5, 15):
        grid[r][10] = 1
    for c in range(5, 20):
        grid[10][c] = 1
    grid[15][15] = 1
    grid[16][15] = 1
    return grid


MAZE = get_hard_maze()
START, END = (2, 2), (ROWS - 3, COLS - 3)

# Data for final graph
stats = {"DFS": 0, "BFS": 0, "GBFS": 0, "ASTAR": 0}


def draw_ui(screen, visited, path, current, name, nodes, font):
    screen.fill(COLOR_BG)

    # Draw Cells
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * GRID_SIZE, r * GRID_SIZE
            color = COLOR_PATH if MAZE[r][c] == 0 else COLOR_WALL

            if (r, c) == START:
                color = (0, 255, 0)  # Start
            elif (r, c) == END:
                color = (255, 0, 0)  # End
            elif (r, c) == current:
                color = COLOR_CURRENT
            elif (r, c) in path:
                color = (255, 165, 0)  # Path
            elif (r, c) in visited:
                color = COLOR_VISITED

            pygame.draw.rect(screen, color, (x, y, GRID_SIZE - 1, GRID_SIZE - 1))

    # Sidebar Explanations
    pygame.draw.rect(screen, (30, 30, 40), (650, 0, 350, HEIGHT))

    # Dynamic logic explanation
    explanations = {
        "BFS": "Checking all neighbors equally. (Layer by Layer)",
        "DFS": "Diving deep into one path until it hits a wall.",
        "GBFS": "Ignoring path cost! Just running toward the red exit.",
        "ASTAR": "Smart balance: Distance from start + distance to end.",
    }

    y_offset = 50
    lines = [
        f"ALGORITHM: {name}",
        f"Nodes Explored: {nodes}",
        f"Path Steps: {len(path)}",
        "",
        "LOGIC:",
        explanations[name],
    ]

    for line in lines:
        img = font.render(line, True, COLOR_TEXT)
        screen.blit(img, (670, y_offset))
        y_offset += 40

    pygame.display.flip()


def run_algo(name, screen, font):
    visited = set()
    nodes_count = 0

    if name == "BFS":
        q = deque([(START, [])])
    elif name == "DFS":
        q = [(START, [])]
    else:
        q = [(0, START, [])]  # Priority Queue

    while q:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # Step extraction
        if name == "BFS":
            curr, path = q.popleft()
        elif name == "DFS":
            curr, path = q.pop()
        else:
            _, curr, path = heapq.heappop(q)

        if curr == END:
            stats[name] = nodes_count
            time.sleep(2)  # Show the final result for 2 seconds
            return

        if curr not in visited:
            visited.add(curr)
            nodes_count += 1

            # Slow down the loop so humans can see it
            time.sleep(TIME_DELAY)
            draw_ui(screen, visited, path, curr, name, nodes_count, font)

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] == 0:
                    new_path = path + [curr]
                    if name in ["BFS", "DFS"]:
                        q.append(((nr, nc), new_path))
                    else:
                        # Heuristic: Manhattan Distance
                        h = abs(nr - END[0]) + abs(nc - END[1])
                        # A* uses (G + H), GBFS uses only H
                        priority = h if name == "GBFS" else (len(new_path) + h)
                        heapq.heappush(q, (priority, (nr, nc), new_path))


# --- EXECUTION ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 22)

for algo in ["BFS", "DFS", "GBFS", "ASTAR"]:
    run_algo(algo, screen, font)

pygame.quit()

# --- FINAL GRAPH ---
plt.figure(figsize=(10, 6))
plt.bar(stats.keys(), stats.values(), color=["blue", "gray", "red", "green"])
plt.title("Which Algorithm was most efficient? (Nodes Explored)")
plt.ylabel("Lower = Smarter")
plt.show()
