from cell import Cell
import maze_runner as mr
from dfs import dfs_traversal
import copy
maze = []

for row in xrange(15):
    maze.append([])
    for col in xrange(15):
        maze[row].append(Cell(0))

maze[0][1].value = 1
for col in range(2, 15, 1):
    maze[5][col].value = 1
maze[6][2].value = 1
for col in range(2, 15, 1):
    maze[11][col].value = 1
maze[12][2].value = 1

mr.visualize_maze(maze)
result = dfs_traversal(maze, 15)
path = mr.get_path(14, 14, copy.deepcopy(maze))
print path
mr.trace_path(copy.deepcopy(maze), path)
fringe = result["fringe"]
print result["max_fringe_length"]
mr.visualize_explored_cells(copy.deepcopy(maze), fringe)



