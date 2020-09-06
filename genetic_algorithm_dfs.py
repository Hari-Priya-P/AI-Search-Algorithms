import maze_runner
import copy
import random
from Queue import PriorityQueue
import numpy as np
from dfs import dfs_traversal
import pandas as pd


def test_population(new_maze_population):
    print "--------------------"
    print "Population Solvability Check"
    for curr_maze_count in range(new_maze_population.qsize()):
        curr_maze = new_maze_population.queue[curr_maze_count]
        curr_maze_result_dict = dfs_traversal(copy.deepcopy(curr_maze[1]), dim)
        if not curr_maze_result_dict["is_solvable"]:
            print "ERROR!!!"
            maze_runner.visualize_maze(copy.deepcopy(curr_maze[1]))
        print curr_maze_result_dict["max_fringe_length"]
    print "--------------------"

# function to swap two columns in a maze
def column_swap(maze, crossover1, crossover2):
    for index in maze:
        maze[crossover1], maze[crossover2] = maze[crossover2], maze[crossover1]

# Main code
dim = 45
p = 0.2

# priority queue with fitness (i.e. hardness) associated with each maze
maze_population = PriorityQueue()

population_size = 50
total_crossovers = 50
mutation_rate = 0.02
generations = 100
population_fitness_vector = []
column_list = ['best_fitness', 'avg_fitness']
# data frame to store the fitness values for analysis purposes
generation_stats_df = pd.DataFrame(columns=column_list)

# generate initial population
for i in range(population_size):
    while True:
        maze = maze_runner.get_maze(dim, p)

        # find path using dfs
        result_dict = dfs_traversal(copy.deepcopy(maze), dim)

        # calculate fitness using the maximum fringe length
        maze_fitness = -result_dict["max_fringe_length"]
        if result_dict["is_solvable"]:
            break

    maze_population.put((maze_fitness, copy.deepcopy(maze)))
    population_fitness_vector.append(-maze_fitness)

print "initial population generated"

# generate children
for generation_count in range(generations):
    print "Generation: ", generation_count
    for crossover_count in range(total_crossovers):
        # if crossover_count%10==0:
        # print crossover_count, " children generated"
        print "Child number: ", crossover_count
        # keep generating child mazes until we find a solvable one
        while True:
            """Approach1: Parents chosen randomly"""
            # choose two parent mazes at random from the population
            """
            parents = random.sample(range(0, population_size), 2)
            parent1_index = parents[0]
            parent2_index = parents[1]
            """

            """Approach2: Parents chosen based on fitness"""
            # assign likehood of getting chosen as a parent
            population_fitness_vector = np.cumsum(population_fitness_vector)
            max_sum = population_fitness_vector[-1]
            # the vector now has the cumulative probability of each cell being chosen as the parent
            population_fitness_vector = [float(cumulative_fitness) / max_sum for
                                         cumulative_fitness in population_fitness_vector]

            random_number = random.random()
            for i in range(population_size):
                if random_number < population_fitness_vector[i]:
                    parent1_index = i
                    break

            while True:
                random_number = random.random()
                for i in range(population_size):
                    if random_number < population_fitness_vector[i]:
                        parent2_index = i
                        break
                # to check for unique parents
                if parent2_index != parent1_index:
                    break

            # combine the parents in some way to get the child maze
            # choose a cross over point randomly
            crossover_point = random.random()
            crossover_row = int(crossover_point * dim)

            # calculate contribution of both parents
            parent1 = np.array(copy.deepcopy(maze_population.queue[parent1_index][1]), dtype=object)
            parent1 = parent1[:crossover_row, :]
            parent2 = np.array(copy.deepcopy(maze_population.queue[parent2_index][1]), dtype=object)
            parent2 = parent2[crossover_row:, :]

            # create child maze by combining the parents row-wise at the cross-over point
            child_maze = np.concatenate((parent1, parent2), axis=0)
            child_maze = child_maze.tolist()

            # mutate the child maze
            mutations = int(mutation_rate * dim)
            for i in range(mutations):
                """Approach1: Randomly flipping the bit"""
                """
                while True:
                    x = random.randint(0, dim-1)
                    y = random.randint(0, dim-1)
                    if not (x==0 and y==0) and not (x==dim-1 and y==dim-1):
                        break
                child_maze[x][y].value = int(not(child_maze[x][y].value))
                """

                # Approach2: Swapping Columns
                mutation_rows = random.sample(range(1, dim - 1), 2)
                column_swap(copy.deepcopy(child_maze), mutation_rows[0], mutation_rows[1])

            print "Mutation Successful"

            # compute the fitness of each child
            child_result_dict = dfs_traversal(copy.deepcopy(child_maze), dim)

            # calculate fitness using the max fringe length
            maze_fitness = -child_result_dict["max_fringe_length"]

            if child_result_dict["is_solvable"]:
                break

        maze_population.put((maze_fitness, copy.deepcopy(child_maze)))

    # create new population using 90% best mazes and 10% from the left-over mazes
    best_mazes_count = int(0.9 * population_size)
    worst_mazes_count = population_size - best_mazes_count
    random_mazes_count = population_size - best_mazes_count
    fitness_average = 0

    new_maze_population = PriorityQueue()
    population_fitness_vector = []

    for count in range(best_mazes_count):
        (fitness, maze) = maze_population.get()
        if count == 0:
            fitness_fittest = fitness
        fitness_average = fitness_average + (fitness - fitness_average) / (count + 1)
        new_maze_population.put((fitness, copy.deepcopy(maze)))
        population_fitness_vector.append(fitness)

    new_gen_random_ind = random.sample(range(0, maze_population.qsize()), random_mazes_count)
    new_gen_random_ind.sort()

    count = 0
    for i in range(maze_population.qsize()):
        (fitness, maze) = maze_population.get()
        if count < len(new_gen_random_ind) and i == new_gen_random_ind[count]:
            new_maze_population.put((fitness, copy.deepcopy(maze)))
            population_fitness_vector.append(fitness)
            fitness_average = fitness_average + (fitness - fitness_average) / (count + 1)
            count += 1
    df_entry = pd.DataFrame([(fitness_fittest, fitness_average)], columns=column_list, index=[generation_count])
    generation_stats_df = generation_stats_df.append(df_entry)
    print "fitness of the fittest maze: ", fitness_fittest
    print "average fitness of the new population: ", fitness_average

    """
    Approach1: We take the weakest 10% of the population to the new population
    # print "fitness of fittest: ", fitness_fittest
    # print "average fitness of fittest population: ", fitness_average
    # while maze_population.qsize()>worst_mazes_count:
    # 	maze_population.get()

    # for count in range(worst_mazes_count):
    # 	(fitness, maze) = maze_population.get()
    # 	if count == worst_mazes_count-1
    # 		fitness_worst = fitness
    # 	new_maze_population.put((fitness, copy.deepcopy(maze)))
    """
    maze_population = new_maze_population

print generation_stats_df
generation_stats_df.to_csv("generation_stats_df.csv")
hardest_maze = maze_population.get()
print "fitness of the hardest maze: ", hardest_maze[0]
maze_runner.visualize_maze(hardest_maze[1])
hardest_maze_result_dict = dfs_traversal(copy.deepcopy(hardest_maze[1]), dim)
maze_runner.visualize_explored_cells(hardest_maze[1], hardest_maze_result_dict["fringe"])
