import pandas as pd
import matplotlib as plt
from matplotlib import pyplot
colors = ['#ffb8a7', '#f05c15', '#59b6eb', '#966842', '#f44747', '#7fdb6a', '#0e68ce', '#6bc5c6', '#f7911f', '#e42f68', '#f98dbe', '#76c158', '#aaaaaa', '#4e8975']

generation_stats_df = pd.read_csv("generation_stats_df_more_gen_1.csv", index_col=0) 
generation_stats_df = generation_stats_df * -1

pyplot.xlabel("Generation")
pyplot.ylabel("Avg fitness")
pyplot.title("Avg fitness v/s Generation")
pyplot.plot(generation_stats_df.index, generation_stats_df["avg_fitness"], marker='o')
pyplot.show()
pyplot.close()

pyplot.xlabel("Generation")
pyplot.ylabel("Highest fitness")
pyplot.title("Highest fitness v/s Generation")
pyplot.plot(generation_stats_df.index, generation_stats_df["best_fitness"], marker='o')
pyplot.show()
pyplot.close()