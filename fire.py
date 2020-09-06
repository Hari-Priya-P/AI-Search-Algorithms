# -*- coding: utf-8 -*-
from cell import Cell
import random
from sets import Set
import math
import copy

# This is used to check if there is a blank space around the
# cell (x, y). This is used to check if a given cell is at 
# the boundry of the fire cluster
def has_no_blank_neighbor(x, y, maze):
	dim = len(maze)
	if(x-1>=0):
		if(maze[x-1][y].value == 0):
			return False
	if(y-1>=0):
		if(maze[x][y-1].value == 0):
			return False
	if(x+1<=dim-1):
		if(maze[x+1][y].value == 0):
			return False	
	if(y+1<=dim-1):
		if(maze[x][y+1].value == 0):
			return False
	return True

# Removes all the false positives so that we are left with the set 
# boundary_cells which just contains all the cells present at the edge
# of the fire cluster
def filter_boundary_cells(boundary_cells, maze):
	new_boundary_cells = set()
	for [x, y] in boundary_cells:
		if not has_no_blank_neighbor(x, y, maze):
			new_boundary_cells.add((x, y))
	boundary_cells = []
	return new_boundary_cells

# Returns the number of neighbors of cell (x, y) which are on fire
def get_number_of_neighbors_on_fire(maze, x, y, dim):
	count = 0
	if(x-1>=0 and maze[x-1][y].value == 2):
		count = count + 1
	if(y-1>=0 and maze[x][y-1].value == 2):
		count = count + 1
	if(x+1<=dim-1 and maze[x+1][y].value == 2):
		count = count + 1
	if(y+1<=dim-1 and maze[x][y+1].value == 2):
		count = count + 1
	return count

# Get all the cells in the maze which are on fire 
def get_fire_cells(maze, dim):
	fire_cells = []
	for i in range(dim):
		for j in range(dim):
			if maze[i][j].value == 2:
				fire_cells.append([i, j])
	return fire_cells

# Adds the neighbors of [x, y] to the set candidate_neighbors. This method is
# used to obtain set of cells which have the potential to catch fire in the 
# following time step
def get_candidate_neighbors(maze, x, y, dim, candidate_neighbors):
	if(x-1>=0 and maze[x-1][y].value != 1):
		candidate_neighbors.add((x-1, y))
	if(y-1>=0 and maze[x][y-1].value != 1):
		candidate_neighbors.add((x, y -1))
	if(x+1<=dim-1 and maze[x+1][y].value != 1):
		candidate_neighbors.add((x+1, y))
	if(y+1<=dim-1 and maze[x][y+1].value != 1):
		candidate_neighbors.add((x, y + 1))
	return candidate_neighbors

# Spreads fire to the cells neighboring burning cells according the procedure mentioned
# in the assignment
def spread_fire(maze, dim, q, boundary_cells):
	# Cells currently on fire
	fire_cells = get_fire_cells(maze, dim)
	# Cells having potential to catch fire in the following time step
	candidate_neighbors = Set([])
	# Cells which will catch fire in the following time step
	new_fire_cells = Set([])
	for [x, y] in fire_cells:
		candidate_neighbors = get_candidate_neighbors(maze, x, y, dim, candidate_neighbors)
	for [x, y] in candidate_neighbors:
		k = get_number_of_neighbors_on_fire(maze, x, y, dim)
		probability =  1.0 - math.pow(1 - q, k)
		if random.random() < probability:
			new_fire_cells.add((x, y))
			# Adding potential cells which would be at the boundry of the fire cluster.
			# Would be filtered to remove the false positives using filter_boundary_cells
			boundary_cells.add((x, y))
	for [x, y] in new_fire_cells:
		# Put cells on fire
		maze[x][y].value = 2
	boundary_cells = filter_boundary_cells(boundary_cells, maze)
	return maze, boundary_cells

# Starts fire at top right cell
def start_fire(maze, dim):
	maze[0][dim - 1] = Cell(2)
	return maze