'''
Similar to the check_neighbours method for BFS except that
this method also checks for the common node in the top fringe
and the bottom fringe which is also a terminating condition
for the BD-BFS algorithm.
'''


def checkneighbours_bbfs(maze, x, y, dim, fringe, closed):
    # intersecting node explored by both top and bottom searches, which signifies that path is found
    intersect = None

    # right neighbour
    if y + 1 < dim and maze[x][y + 1].value != 1 and (x, y + 1) not in closed and (x, y+1) not in fringe:
        if maze[x][y + 1].parent is not None:
            intersect = (x, y + 1)
        else:
            fringe.append((x, y + 1))
            maze[x][y + 1].parent = (x, y)
    # bottom neighbour
    if x + 1 < dim and maze[x + 1][y].value != 1 and (x + 1, y) not in closed and (x+1, y) not in fringe:
        if maze[x + 1][y].parent is not None:
            intersect = (x + 1, y)
        else:
            fringe.append((x + 1, y))
            maze[x + 1][y].parent = (x, y)
    # left neighbour
    if y - 1 >= 0 and maze[x][y - 1].value != 1 and (x, y - 1) not in closed and (x, y-1) not in fringe:
        if maze[x][y - 1].parent is not None:
            intersect = (x, y - 1)
        else:
            fringe.append((x, y - 1))
            maze[x][y - 1].parent = (x, y)
    # top neighbour
    if x - 1 >= 0 and maze[x - 1][y].value != 1 and (x - 1, y) not in closed and (x-1, y) not in fringe:
        if maze[x - 1][y].parent is not None:
            intersect = (x - 1, y)
        else:
            fringe.append((x - 1, y))
            maze[x - 1][y].parent = (x, y)

    return intersect
