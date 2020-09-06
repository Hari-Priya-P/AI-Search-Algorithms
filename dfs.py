from maze_runner import get_maze
from maze_runner import get_path
from maze_runner import trace_path

"""
checks for valid neighbours which are not present and in
the closed set and adds them to the fringe. Following is the 
order in which the neighbors are added to the fringe:
	1) up
	2) left
	3) down
	4) right
Since the fringe is implemented using stack data structure,
the order in which these neighbors are popped out is opposite
thus making sure that we always try to go towards bottom right
side of the fringe, ie. towards the goal.
"""


def get_neighbors(maze, x, y, dim, closed_set, fringe):
	if x-1 >= 0:
		if maze[x-1][y].value != 1 and (x-1, y) not in closed_set and not maze[x-1][y].visited:
			maze[x-1][y].visited = True
			maze[x-1][y].parent = (x, y)
			fringe.append((x-1, y))
	if y-1 >= 0:
		if maze[x][y-1].value != 1 and (x, y-1) not in closed_set and not maze[x][y-1].visited:
			maze[x][y-1].visited = True
			maze[x][y-1].parent = (x, y)
			fringe.append((x, y-1))
	if x+1 <= dim-1:
		if maze[x+1][y].value != 1 and (x+1, y) not in closed_set and not maze[x+1][y].visited:
			maze[x+1][y].visited = True
			maze[x+1][y].parent = (x, y)
			fringe.append((x+1, y))		
	if y+1 <= dim-1:
		if maze[x][y+1].value != 1 and (x, y+1) not in closed_set and not maze[x][y+1].visited:
			maze[x][y+1].visited = True
			maze[x][y+1].parent = (x, y)
			fringe.append((x, y+1))	
	return fringe


# traverses the graph using DFS algorithm
def dfs_traversal(maze, dim):
	closed_set = set()
	fringe = [(0,0)]
	# To record the max size of the fringe during exploration
	max_fringe_length = 0
	exploration_steps = 0
	avg_fringe_length = 0
	while len(fringe) > 0:
		(x, y) = fringe.pop()
		exploration_steps = exploration_steps + 1
		if (x, y) in closed_set:
			# No need to explore elements in the closed set
			continue
		if (x, y) == (dim-1, dim-1):
			# Solution found
			result_dict = {
				"is_solvable": True,
				"total_steps": exploration_steps,
				"max_fringe_length": max_fringe_length,
				"avg_fringe_length": avg_fringe_length,
				"closed_set": closed_set
			}
			return result_dict
		fringe = get_neighbors(maze, x, y, dim, closed_set, fringe)
		fringe_length = len(fringe)
		if fringe_length > max_fringe_length:
			max_fringe_length = fringe_length
		avg_fringe_length = avg_fringe_length + (fringe_length - avg_fringe_length) / exploration_steps
		closed_set.add((x, y))
	print "No Solution"
	result_dict = {
		"is_solvable": False,
		"total_steps": exploration_steps,
		"max_fringe_length": max_fringe_length,
		"avg_fringe_length": avg_fringe_length,
		"closed_set": closed_set
	}
	return result_dict

# dim = 10
# p = 0.2
# maze = get_maze(dim, p)
# result = dfs_traversal(maze, dim)
# if result["is_solvable"]:
# 	path = get_path(dim-1, dim-1, maze)
# 	print "Path length: " + str((len(path)))
# 	trace_path(maze, path)