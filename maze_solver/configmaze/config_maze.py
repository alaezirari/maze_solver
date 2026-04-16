# ========================================================================#
#                      CONFIGURATION DU LABYRINTHE                       #
# ========================================================================#


# definir le labyrinthe aleatoirement:
import random


def generate_maze(width, height, path, start, goal):
    """
    generate a random maze with the given width and height, and a path from start to goal
    parameters:
    width (int): the width of the maze
    height (int): the height of the maze
    path (list of tuples): a predefined path asa listof (x,y) coordinates
    start (tuple): the starting point (x,y) of the maze
    goal (tuple): the goal point (x,y) of the maze.

    returns:
    dict: a dictionary representing the maze
    """
    maze = {}
    # initialise the maze with random walls (1) and open spaces (0)
    for y in range(height):
        for x in range(width):
            maze[(x, y)] = 1  # random.choice([0,1])
    # ensure the predifined , start, and goal are open
    for coord in path:
        maze[coord] = 0

    maze[start] = 0
    maze[goal] = 0
    return maze


# example usage
width = 100
height = 10
start = (0, 0)
goal = (9, 9)


def initialize_path(path, width, height):
    i, j = 0, 0
    for i in range(0, height // 2):
        path.append((i, j))

    for j in range(0, int(width / 2)):
        path.append((i, j))
    for i in range(0, height // 2):
        path.append((i, j))
    for j in range(width // 2, width - 1):
        path.append((0, j))
    for i in range(0, height):
        path.append(
            (i, width - 1)
        )  # attentin: width-1 and not width because of initialization!!
    return path


path = []
path = initialize_path(path, width, height)
maze = config_maze.generate_maze(width, height, path, start, goal)
