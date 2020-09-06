from maze_runner import get_maze
from bfs_2 import bfs_traversal
import time
import matplotlib.pyplot as plt
from matplotlib import pyplot
import pandas as pd
import scipy.interpolate
from a_star import a_star_traversal

''' 
Returns the average execution time for bfs traversals and
also the total number of tries to get 100 success cases
'''
def get_avg_times_and_total_tries(dim, p):
	total_time = 0
	avg_time = 0.0
	success_count = 0
	max_avg_time = 0
	totaltries = 0

	for i in xrange(0, 100):
		while(True):
			test_maze = get_maze(dim, p)
			totaltries = totaltries + 1
			startTime = time.time()
			result_dict = a_star_traversal(test_maze, "manhattan")
			end_time = time.time()
			if result_dict["is_solvable"]:
				time_taken = end_time - startTime 
				avg_time = avg_time + (time_taken - avg_time)/(success_count + 1)
				total_time += time_taken
				success_count = success_count + 1
				# print "Success count: " + str(success_count)
				break	
		
	return avg_time, total_time, totaltries

# Plots the total time taken to complete 100 success cases versus P value for different dimensions 
def generate_comparison_dataframes(dim_list, p_list):
	avgtime_df = pd.DataFrame(columns=p_list, index=dim_list)
	runtime_df = pd.DataFrame(columns=p_list, index=dim_list)
	totaltries_df = pd.DataFrame(columns=p_list, index=dim_list)

	for ind, dim in enumerate(dim_list):
		avg_time_list = []
		run_time_list = []
		totaltries_list = []

		for p in p_list:
			print dim, p
			avg_time, run_time, totaltries = get_avg_times_and_total_tries(dim, p)
			avg_time_list.append(avg_time)
			run_time_list.append(run_time)
			totaltries_list.append(totaltries)

		avgtime_df.iloc[ind] = pd.Series(avg_time_list, index=avgtime_df.columns)
		runtime_df.iloc[ind] = pd.Series(run_time_list, index=runtime_df.columns)
		totaltries_df.iloc[ind] = pd.Series(totaltries_list, index=totaltries_df.columns)

	return avgtime_df, runtime_df, totaltries_df

# Gets the solvability in % for a particular dim and range of p values
def get_solvability(dim, p):
	total_time, totaltries = get_avg_times_and_total_tries(dim, prob)
	print "Solvability with p = " + str(prob) + " = " + str(100*100.0/totaltries)


def plot(dataframe, plot_xlabel, plot_ylabel, plot_title, plot_legend_label, plot_legend_value):
	# colors = ['blue', 'red', 'green', 'yellow', 'black', 'cyan', 'pink', '']
	colors = ['#ffb8a7', '#f05c15', '#59b6eb', '#966842', '#f44747', '#7fdb6a', '#0e68ce', '#6bc5c6', '#f7911f', '#e42f68', '#f98dbe', '#76c158', '#aaaaaa', '#4e8975']
	
	pyplot.xlabel(plot_xlabel)
	pyplot.ylabel(plot_ylabel)
	plt.title(plot_title)
	for i in range(dataframe.shape[0]):
		plt.plot(dataframe.iloc[i].index, dataframe.iloc[i].values, 
			label=plot_legend_label+"=%f"%(plot_legend_value[i]), marker='o', color=colors[i])
	plt.legend()
	plt.show()

# Main
 
# dim_list = [10, 20]
# dim_list = [10, 50, 100, 125]
dim_list = [10, 50, 100, 120, 125, 150, 175]

# p_list = [0.1, 0.2]
p_list = [0.1, 0.125, 0.15, 0.175, 0.20, 0.225, 0.25, 0.275, 0.30, 0.325, 0.35, 0.375, 0.40]

avgtime_df, runtime_df, totaltries_df = generate_comparison_dataframes(dim_list, p_list)
avgtime_df.to_csv("avgtime_df.csv")
runtime_df.to_csv("runtime_df.csv")
totaltries_df.to_csv("totaltries_df.csv")

solvabilty_df = pd.DataFrame(columns=p_list, index=dim_list)
for ind, dim in enumerate(dim_list):
	solvability_list = []
	for p in p_list:
		solvability_list.append(100*100.0/totaltries_df.loc[dim][p])
	solvabilty_df.iloc[ind] = pd.Series(solvability_list, index=totaltries_df.columns)
solvabilty_df.to_csv("solvabilty_df.csv")

# Read files from the csv saved and plot the relavant information
csv1 = pd.read_csv("avgtime_df.csv", index_col=0) 
csv2 = pd.read_csv("runtime_df.csv", index_col=0) 
csv3 = pd.read_csv("totaltries_df.csv", index_col=0) 
csv4 = pd.read_csv("solvabilty_df.csv", index_col=0) 

# Plot the relavant data
plot(dataframe=csv1, plot_legend_label="dim", plot_title="Avg runtime v/s Probabilty", plot_xlabel="Probabilty p", plot_ylabel="Avg runtime (s)", plot_legend_value = [10, 50, 100, 125, 150, 175])
plot(dataframe=csv1.transpose(), plot_legend_label="p", plot_title="Avg runtime v/s Dimension", plot_xlabel="Dimension", plot_ylabel="Avg runtime (s)", plot_legend_value=[0.1, 0.125, 0.15, 0.175, 0.20, 0.225, 0.25, 0.275, 0.30, 0.325, 0.35, 0.375, 0.40])

plot(dataframe=csv4, plot_legend_label="dim", plot_title="Solvability v/s Probabilty", plot_xlabel="Probabilty p", plot_ylabel="Solvability(%)", plot_legend_value = [10, 50, 100, 125, 150, 175])
plot(dataframe=csv4.transpose(), plot_legend_label="p", plot_title="Solvability v/s Dimension", plot_xlabel="Dimension", plot_ylabel="Solvability(%)", plot_legend_value=[0.1, 0.125, 0.15, 0.175, 0.20, 0.225, 0.25, 0.275, 0.30, 0.325, 0.35, 0.375, 0.40])

