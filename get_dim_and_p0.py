from maze_runner import get_maze
from bfs_2 import bfs_traversal
import time
import matplotlib.pyplot as plt
import pandas as pd
import scipy.interpolate

''' 
Returns the average execution time for bfs traversals and
also the total number of tries to get 100 success cases
'''
def get_avg_times_and_total_tries(dim, p, mainstart_time):
	# Contains average time for each of the successful atempts at path finding
	avg_times = []
	# Records the avergae time to solve a particular solvable maze
	avg_time = 0.0
	# Total number of mazes solved / solvable mazes encountered
	success_count = 0
	maze = get_maze(dim, p)
	# Records the maximum value present in the list: avg_times
	max_avg_time = 0
	# Records total numnber of tries which includes both solvable and insolvable mazes
	totaltries = 0
	for i in xrange(0, 100):
		startTime = time.time()
		while(True):
			totaltries = totaltries + 1
			if bfs_traversal(maze, dim):
				time_taken = time.time() - startTime 
				avg_time = (avg_time*success_count+(time_taken))/(success_count + 1)
				success_count = success_count + 1
				print "Success count: " + str(success_count)
				avg_times.append(avg_time) 
				if max_avg_time < avg_time:
					max_avg_time = avg_time
				break
			maze = get_maze(dim, p)
		maze = get_maze(dim, p)
	
	plt.plot(avg_times)
	plt.ylabel("Average execution time in seconds")
	plt.xlabel("Number of successful executions")
	plt.annotate("last average = " + str(round(avg_times[len(avg_times)-1], 6)),
         xy=(100, avg_times[len(avg_times)-1]), xytext=(60, max_avg_time),
         arrowprops=dict(facecolor='black', shrink=0.005),)
	total_timetaken = time.time() - mainstart_time
	plt.title("Dim = " + str(dim) + " P = " + str(p) + " (Total time taken: " + 
		str(round(total_timetaken, 2)) + " seconds)")
	plt.show()
	return totaltries

# Plots the total time taken to complete 100 success cases versus P value for different dimensions 
def generate_comparison_plot():
	df=pd.DataFrame({'x': [0.25, 0.3, 0.35, 0.4], 'Dim = 60': [2.48, 2.75, 4.83, 21.56], 'Dim = 80': [4.15, 4.77, 8.81, 57.44], 'Dim = 120': [11.2, 11.83, 18.3, 134.41], 'Dim = 170': [21.7, 26.26, 33.99, 380.31], 'Dim = 240': [50.5, 59.58, 80.1, 1138.9] })
	plt.ylabel("Execution time for discovering and solving 100 mazes")
	plt.xlabel("P")
	plt.title("Total execution time versus P")
	plt.plot( 'x', 'Dim = 60', data=df, marker='o', color='blue')
	plt.plot( 'x', 'Dim = 80', data=df, marker='o', color='red')
	plt.plot( 'x', 'Dim = 120', data=df, marker='o', color='green')
	plt.plot( 'x', 'Dim = 170', data=df, marker='o', color='yellow')
	plt.plot( 'x', 'Dim = 240', data=df, marker='o', color='black')
	plt.legend()
	plt.show()

# Gets the solvability in % for a particular dim and range of p values
def get_solvability(dim, p_array):
	for prob in p_array:
		totaltries = get_avg_times_and_total_tries(dim, prob, mainstart_time)
		print "Solvability with p = " + str(prob) + " = " + str(100*100.0/totaltries)

# Plots Success rate versus P value graph to obtain the P0 value
def get_po_value():
	p_values = [0.1, 0.125, 0.15, 0.175, 0.20, 0.225, 0.25, 0.275, 0.30, 0.325, 0.35, 0.375, 0.40]
	solvabilities = [97.09, 94.34, 92.59, 91.74, 81.97, 74.07, 64.52, 60.61, 54.64, 36.50, 26.39, 11.53, 1.73]
	p_value_interp = scipy.interpolate.interp1d(solvabilities, p_values)
	p0 = p_value_interp(50)
	plt.plot(p_values, solvabilities)
	plt.annotate("P0 = " + str(round(p0, 3)) + " (success rate = 50%)",
	     xy=(p0, 50), xytext=(p0 - 0.1, p0 - 0.04),
	     arrowprops=dict(facecolor='black', shrink=0.005),)
	plt.ylabel("Success rate in %")
	plt.xlabel("P value")
	plt.title("Success rate versus probability")
	plt.show()

mainstart_time = time.time()
'''
Values of p tried: [0.25, 0.3, 0.35, 0.4]
Values of dim tried: [60, 80, 120, 170, 240]
get_avg_times_and_total_tries(dim, p, mainstart_time)
generate_comparison_plot - for comparison between each of the dims
chosen dim: 120
'''

'''
p_array = [0.1, 0.125, 0.15, 0.175, 0.20, 0.225, 0.25, 0.275, 0.30, 0.325, 0.35, 0.375, 0.40]
get_solvability(dim, p_array)
get_po_value()
'''