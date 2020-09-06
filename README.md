# AI-Search-Algorithms

This project is intended as an exploration of various search algorithms, both in the traditional application of path planning, and more abstractly in the construction and design of complex objects.

## 1. Environments and Algorithms

The environment is a map which is a square grid of cells/locations, where each cell is either empty or occupied. An agent wishes to travel from the upper left corner to the lower right corner, along the shortest path possible. The agent can only move from empty cells to neighboring empty cells in the up/down direction, or left/right - each cell has potentially four neighbors. Find the shortest path possible using the following algorithms: <br/>
- Depth-First Search<br/>
- Breadth-First Search<br/>
- A*, where the heuristic is to estimate the distance remaining via the Euclidean Distance<br/>
- A∗, where the heuristic is to estimate the distance remaining via the Manhattan Distance<br/>
- Bi-Directional Breadth-First Search<br/>
For any specified map, applying one of these search algorithms should either return failure, or a path from start to goal in terms of a list of cells taken.<br/>

## 2. Analysis and Comparison

Having coded five path-generating algorithms, we want to analyze and compare their performance. This is important not only for theoretical reasons, but also to check to make sure that your algorithms are behaving as they should.<br/>
- Find a map size (dim) that is large enough to produce maps that require some work to solve, but small enough that you can run each algorithm multiple times for a range of possible p values. How did you pick a dim? <br/>
- For p ≈ 0.2, generate a solvable map, and show the paths returned for each algorithm. Do the results make sense? <br/>
- Given dim, how does maze-solvability depend on p? For a range of p values, estimate the probability that a maze will be solvable by generating multiple mazes and checking them for solvability. What is the best algorithm to use here? Plot density vs solvability, and try to identify as accurately as you can the threshold p0 where for p < p0, most mazes are solvable, but p > p0, most mazes are not solvable. <br/>
- For p in [0, p0] as above, estimate the average or expected length of the shortest path from start to goal. You may discard unsolvable maps. Plot density vs expected shortest path length. What algorithm is most useful here? <br/>
- Is one heuristic uniformly better than the other for running A∗ ? How can they be compared? Plot the relevant data and justify your conclusions. <br/>
- Do these algorithms behave as they should? <br/>
- For DFS, can you improve the performance of the algorithm by choosing what order to load the neighboring rooms into the fringe? What neighbors are ‘worth’ looking at before others? <br/>
- On the same map, are there ever nodes that BD-DFS expands that A∗ doesn’t? Why or why not? Give an example, and justify. <br/>
- How does the threshold probability p0 depend on dim?<br/>

## 3. Generating Hard Mazes

Generated hard mazes using Genetic Algorithm with the following algorithms using the paired metric:<br/>
- DFS with Maximal Fringe Size<br/>
- A*-Manhattan with Maximal Nodes Expanded<br/>

## 4. What If The Maze Were On Fire?

Consider the following model of the maze being on fire and solve it using the search algorithms: any cell in the maze is either ‘open’, ‘blocked’, or ‘on fire’. Starting out, the upper right corner of the maze is on fire. You can move between open cells or choose to stay in place, once per time step. You cannot move into cells that are on fire, and if your cell catches on fire you die. But
each time-step, the fire may spread, according to the following rules: For some ‘flammability rate’ 0 ≤ q ≤ 1<br/>
- If a free cell has no burning neighbors, it will still be free in the next time step.
- If a cell is on fire, it will still be on fire in the next time step.
- If a free cell has k burning neighbors, it will be on fire in the next time step with probability 1 − (1 − q)<sup>k</sup>.<br/>
