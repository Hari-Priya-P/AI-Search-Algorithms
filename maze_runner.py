import random
from cell import Cell

# import the visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# returns maze with dimension dim with probability p of a cell being occupied
def get_maze(dim, p):
	maze = []
	for row in xrange(dim):
		maze.append([])
		for col in xrange(dim):
			if random.random()<p:
				# occupied cell
				maze[row].append(Cell(1))
			else:
				# empty cell
				maze[row].append(Cell(0))

	# start cell
	maze[0][0] = Cell(0) 
	# goal cell
	maze[dim-1][dim-1] = Cell(0) 
	return maze

# backtraces the path from destiantion till source
def get_path(x, y, maze):
	path = []
	while((x,y)!=(0,0)):
		path.insert(0,(x,y))
		(x, y) = maze[x][y].parent
	path.insert(0,(0,0))
	return path

# backtraces the path from point (x, y) till point (a, b) 
def get_path_from_a_b(x, y, maze, a, b):
	path = []
	while((x,y)!=(a,b)):
		path.insert(0,(x,y))
		(x, y) = maze[x][y].parent
	path.insert(0,(a,b))
	return path

# visualises the random maze generated
def visualize_maze(maze):
	basic_maze = []
	dim = len(maze)
	for i in range(len(maze)):
		basic_maze.append([])
		for j in range(len(maze[0])):
			basic_maze[i].append(maze[i][j].value)

	basic_maze[0][0]=0
	basic_maze[dim-1][dim-1]=0
	ax = sns.heatmap(basic_maze, cmap="Blues", cbar=False, linewidths=.1, linecolor="Black")
	plt.show()
	plt.close()


# visualises the random maze generated
def visualize_explored_cells(maze, closed_set):
	basic_maze = []
	dim = len(maze)

	for i in range(len(maze)):
		basic_maze.append([])
		for j in range(len(maze[0])):
			basic_maze[i].append(maze[i][j].value)

	for coordinates in closed_set:
		basic_maze[coordinates[0]][coordinates[1]] = 0.5

	plt.figure()
	# cmap=ListedColormap(['cornsilk', 'royalblue', 'grey'])
	ax = sns.heatmap(basic_maze, cmap="Blues", cbar=False, linewidths=.1, linecolor="Black")
	plt.show()
	plt.close()


# visulaises the path from source to destination in the maze 
def trace_path(maze, path):
	basic_maze = []
	for i in range(len(maze)):
		basic_maze.append([])
		for j in range(len(maze[0])):
			basic_maze[i].append(maze[i][j].value)

	for i in range(len(path)):
		coordinates = path[i]
		'''
		Cell value 1.5 is used to denote the point where we catch fire. Thus keeping
		it as 1.5 to distinguish it from other cells in the path.
		'''
		if (basic_maze[coordinates[0]][coordinates[1]] == 1.5):
			basic_maze[coordinates[0]][coordinates[1]] = 1.5
		else:
			basic_maze[coordinates[0]][coordinates[1]] = 0.5
	ax = sns.heatmap(basic_maze, cmap="Blues", cbar=False, linewidths=.1, linecolor="Black")
	plt.show()
	plt.close()