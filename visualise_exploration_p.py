import maze_runner
from a_star import a_star_traversal

dim = 50
steps_p = []
p_list = [0, 0.1, 0.15, 0.2, 0.25, 0.3]

for p in p_list:
	steps = 0
	for i in range(10):
		while(True):
			test_maze = maze_runner.get_maze(dim, p)
			result_dict = a_star_traversal(test_maze, "manhattan")
			if result_dict["is_solvable"]:
				curr_steps = len(result_dict["closed_set"])
				steps+=curr_steps
				break
	steps_p.append(steps/10)
steps_p = steps_p	

pyplot.xlabel("P")
pyplot.ylabel("Exploration Steps")
pyplot.title("Exploration Steps v/s p for dim=50")
pyplot.plot(p_list, steps_p, marker='o')
plt.show()