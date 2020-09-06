"""
- Identify valid neighbours which are unvisited and unexplored for the current cell
- Add the neighbours to the fringe
- Set the parent as current cell for tracing the final path
"""


def check_neighbours(maze, dim, x, y, fringe, closed):
    # right neighbour
    if y + 1 < dim and maze[x][y + 1].value != 1 and not maze[x][y + 1].visited and (x, y + 1) not in closed:
        fringe.append((x, y + 1))
        maze[x][y + 1].visited = True
        maze[x][y + 1].parent = (x, y)
    # bottom neighbour
    if x + 1 < dim and maze[x + 1][y].value != 1 and not maze[x + 1][y].visited and (x + 1, y) not in closed:
        fringe.append((x + 1, y))
        maze[x + 1][y].visited = True
        maze[x + 1][y].parent = (x, y)
    # left neighbour
    if y - 1 >= 0 and maze[x][y - 1].value != 1 and not maze[x][y - 1].visited and (x, y - 1) not in closed:
        fringe.append((x, y - 1))
        maze[x][y - 1].visited = True
        maze[x][y - 1].parent = (x, y)
    # top neighbour
    if x - 1 >= 0 and maze[x - 1][y].value != 1 and not maze[x - 1][y].visited and (x - 1, y) not in closed:
        fringe.append((x - 1, y))
        maze[x - 1][y].visited = True
        maze[x - 1][y].parent = (x, y)

