# example usage
from configmaze import config_maze

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
