from maze_runner import get_maze
from fire_solution import fire_traversal
from a_star import a_star_traversal_with_fire
import matplotlib.pyplot as plt
import pandas as pd
import copy 
import maze_runner as mr

# Get the array with values of q to be used to do the comparison between the baseline
# algorithm and the proposed algorithm. The q value starts with 'start' and has jumps
# of 'jump' and the total size of the array is 'size'
def get_q_array(start, jump, size):
	q_array = []
	value = start
	for x in xrange(size):
		q_array.append(round(value, 2))
		value = value + jump
	return q_array

# For a given value of p, q, and dim, this method generates 100 mazes and runs the baseline
# and the proposed algorithm on the mazes to compute success rate for both the algorithms
def get_success_rate(p, q, dim):
	success_count_proposed = 0
	success_count_a_star = 0
	for x in xrange(100):
		maze_proposed = get_maze(dim, p)
		maze_a_star = copy.deepcopy(maze_proposed)
		manhattan_result_proposed, manhattan_steps, manhattan_max_fringe_length, manhattan_avg_fringe_length, manhattan_closed_set, x_cord, y_cord = fire_traversal(maze_proposed, q)
		manhattan_result_a_star, manhattan_steps, manhattan_max_fringe_length, manhattan_avg_fringe_length, manhattan_closed_set, x_cord, y_cord = a_star_traversal_with_fire(maze_a_star, "manhattan", q)
		if manhattan_result_proposed == 1:
			success_count_proposed = success_count_proposed + 1
		if manhattan_result_a_star == 1:
			success_count_a_star = success_count_a_star + 1
	return success_count_proposed, success_count_a_star

# Obtains success rate in % for baseline algorithm and the proposed algorithm over a range
# of q values 
def get_success_rate_over_range_of_q(p, dim, start, jump, size):
	q_array = get_q_array(start, jump, size)
	success_rates_proposed = []
	success_rates_a_star = []
	for q in q_array:
		print q
		success_count_proposed, success_count_a_star = get_success_rate(p, q, dim)
		success_rates_proposed.append(success_count_proposed)
		success_rates_a_star.append(success_count_a_star)
	return q_array, success_rates_proposed, success_rates_a_star

'''
dim = 50
p = 0.2
start = 0.05
jump = 0.05
size = 12

q_array, success_rates_proposed, success_rates_a_star = get_success_rate_over_range_of_q(p, dim, start, jump, size)
print q_array
print success_rates_proposed
print success_rates_a_star
df=pd.DataFrame({'x': q_array, 'Proposed Algorithm': success_rates_proposed, 'A_star': success_rates_a_star})
plt.ylabel("Success rate in % (averaged over 100 runs)")
plt.xlabel("Q value")
plt.title("Success rate versus q value at dim = 50 and p = 0.2")
plt.plot( 'x', 'Proposed Algorithm', data=df, marker='o', color='blue')
plt.plot( 'x', 'A_star', data=df, marker='o', color='red')
plt.legend()
plt.show()
'''

'''
dim = 30
p = 0.20
q = 0.2
maze_proposed = get_maze(dim, p)
maze_a_star = copy.deepcopy(maze_proposed)
manhattan_result_proposed, manhattan_steps, manhattan_max_fringe_length, manhattan_avg_fringe_length, manhattan_closed_set, x_cord_p, y_cord_p = fire_traversal(maze_proposed, q)
manhattan_result_a_star, manhattan_steps, manhattan_max_fringe_length, manhattan_avg_fringe_length, manhattan_closed_set, x_cord_a, y_cord_a = a_star_traversal_with_fire(maze_a_star, "manhattan", q)

print "a_star: " + str(manhattan_result_a_star)
print "proposed: " + str(manhattan_result_proposed)

if manhattan_result_a_star == 1:
	print "Solution found"
	path = mr.get_path(dim-1, dim-1, maze_a_star)
	mr.trace_path(maze_a_star, path)
elif manhattan_result_a_star == 0:
	print "Solution not found"
	mr.visualize_maze(maze_a_star)
else:
	print "Burnt at " + str(x_cord_a) + ", " + str(y_cord_a)
	maze_a_star[x_cord_a][y_cord_a].value = 1.5
	path = mr.get_path(x_cord_a, y_cord_a, maze_a_star)
	mr.trace_path(maze_a_star, path)

if manhattan_result_proposed == 1:
	print "Solution found"
	path = mr.get_path(dim-1, dim-1, maze_proposed)
	mr.trace_path(maze_proposed, path)
elif manhattan_result_proposed == 0:
	print "Solution not found"
	mr.visualize_maze(maze_proposed)
else:
	print "Burnt at " + str(x_cord_p) + ", " + str(y_cord_p)
	maze_proposed[x_cord_p][y_cord_p].value = 1.5
	path = mr.get_path(x_cord_p, y_cord_p, maze_proposed)
	mr.trace_path(maze_proposed, path)
'''