import maze_runner
import CheckNeighbours_BBFS
from collections import deque
'''
dim = 120
probability = 0.34
maze = maze_runner.get_maze(dim, probability)
'''

def bd_bfs (maze, dim):
    fringe1 = deque()
    fringe2 = deque()
    closed1 = []
    closed2 = []
    fringe1.append((0, 0))
    fringe2.append((dim - 1, dim - 1))
    maze[0][0].parent = None
    maze[dim - 1][dim - 1].parent = None
    max_fringe_length = 0
    avg_fringe_length = 0
    exploration_steps = 0
    result = 0
    while len(fringe1) != 0 and len(fringe2) != 0:
        current1 = fringe1.popleft()
        exploration_steps = exploration_steps + 1
        m1 = current1[0]
        n1 = current1[1]
        if current1 not in closed1:
            if maze[m1][n1].value != 1:
                intersect1 = CheckNeighbours_BBFS.checkneighbours_bbfs(maze, m1, n1, dim, fringe1, closed1)
                if intersect1 is not None:
                    # print "Intersecting node 1:", intersect1
                    result = 1
                    break
                closed1.append((m1, n1))

        current2 = fringe2.popleft()
        exploration_steps = exploration_steps + 1
        m2 = current2[0]
        n2 = current2[1]
        if current2 not in closed2:
            if maze[m2][n2].value != 1:
                intersect2 = CheckNeighbours_BBFS.checkneighbours_bbfs(maze, m2, n2, dim, fringe2, closed2)
                if intersect2 is not None:
                    # print "Intersecting node 2:", intersect2
                    result = 1
                    break
                closed2.append((m2, n2))
        closed_set = closed1 + closed2
        fringe_length = len(fringe1) + len(fringe2)
        avg_fringe_length = avg_fringe_length + (fringe_length - avg_fringe_length) / exploration_steps
        if fringe_length > max_fringe_length:
            max_fringe_length = fringe_length

    if result == 0:
        result_dict = {
            "is_solvable": False,
            "total_steps": exploration_steps,
            "max_fringe_length": max_fringe_length,
            "avg_fringe_length": avg_fringe_length,
            "closed_set": closed_set
        }
        return result_dict
    else:
        path1 = []
        path2 = []
        if intersect1 is not None:
            path1 = maze_runner.get_path(current1[0], current1[1], maze)
            while intersect1[0] <= dim - 1 and intersect1[1] <= dim - 1:
                path2.append(intersect1)
                if intersect1 == (dim - 1, dim - 1):
                    break
                intersect1 = maze[intersect1[0]][intersect1[1]].parent
            # maze_runner.trace_path_bbfs(maze, path1, path2)

        elif intersect2 is not None:
            path1 = maze_runner.get_path(intersect2[0], intersect2[1], maze)
            while current2[0] <= dim - 1 and current2[1] <= dim - 1:
                path2.append(current2)
                if current2 == (dim - 1, dim - 1):
                    break
                current2 = maze[current2[0]][current2[1]].parent
            # maze_runner.trace_path_bbfs(maze, path2, path1)
        # print path
        # print len(path)

        result_dict = {
            "is_solvable": True,
            "total_steps": exploration_steps,
            "max_fringe_length": max_fringe_length,
            "avg_fringe_length": avg_fringe_length,
            "closed_set": closed_set,
            "path_length": len(path1)+len(path2)
        }
        return result_dict

# dim = 10
# p = 0.1
# maze = maze_runner.get_maze(dim, p)
# result_bbfs = bd_bfs(maze, dim)
# print result_bbfs



