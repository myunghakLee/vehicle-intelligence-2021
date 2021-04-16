import numpy as np
import itertools

# Given map
grid = np.array([
    [1, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1]
])

# List of possible actions defined in terms of changes in
# the coordinates (y, x)
forward = [
    (-1,  0),   # Up
    ( 0, -1),   # Left
    ( 1,  0),   # Down
    ( 0,  1),   # Right
]

# Three actions are defined:
# - right turn & move forward
# - straight forward
# - left turn & move forward
# Note that each action transforms the orientation along the
# forward array defined above.
action = [-1, 0, 1]
action_name = ['R', '#', 'L']

init = (4, 3, 0)    # Representing (y, x, o), where
                    # o denotes the orientation as follows:
                    # 0: up
                    # 1: left
                    # 2: down
                    # 3: right
                    # Note that this order corresponds to forward above.
goal = (2, 0)
cost = (2, 1, 20)   # Cost for each action (right, straight, left)

# EXAMPLE OUTPUT:
# calling optimum_policy_2D with the given parameters should return
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]

def optimum_policy_2D(grid, init, goal, cost):
    """
    grid:  [[1 1 1 0 0 0]
            [1 1 1 0 1 0]
            [0 0 0 0 0 0]
            [1 1 1 0 1 1]
            [1 1 1 0 1 1]]
    init:  (4, 3, 0)
    goal:  (2, 0)
    cost:  (2, 1, 20)

    """

    # Initialize the value function with (infeasibly) high costs.
    value = np.full((4, ) + grid.shape, 999, dtype=np.int32)
    # Initialize the policy function with negative (unused) values.
    policy = np.full((4,) + grid.shape, -1, dtype=np.int32)
    # Final path policy will be in 2D, instead of 3D.
    policy2D = np.full(grid.shape, ' ')

    # Apply dynamic programming with the flag change.
    change = True
    while change:
        change = False
        # This will provide a useful iterator for the state space.
        p = itertools.product(
            range(grid.shape[0]),
            range(grid.shape[1]),
            range(len(forward))
        )

        # Compute the value function for each state and
        # update policy function accordingly.
        for y, x, t in p:
            # Mark the final state with a special value that we will
            # use in generating the final path policy.
            if (y, x) == goal and value[(t, y, x)] > 0:
                value[(t, y, x)], policy[(t, y, x)] = 0, -999
                change = True
            elif grid[(y, x)] == 0:
                for i in range(len(action)):
                    index = (t+action[i])%4
                    cx = x + forward[index][1]
                    cy = y + forward[index][0]

                    if 0<= cx < len(grid[0]) and 0 <= cy <len(grid) and (not grid[cy][cx]):
                        cv = value[index][cy][cx] + cost[i]
                        if cv < value[t][y][x]:
                            value[t][y][x] = cv
                            policy[t][y][x] = action[i]
                            change = True

    y, x, o = init


    # print(policy)

    policy2D[(y, x)] = policy[(o, y, x)]
    # print(policy2D)

    while policy[(o, y, x)] != -999:
        p = policy[(o, y, x)]

        co = (o+p) %4
        policy2D[y][x] = action_name[p+1]

        x += forward[co][1]
        y += forward[co][0]
        o = co

        policy2D[y][x] = policy[o][y][x]

    policy2D[y][x] = "*"
    return policy2D

print(optimum_policy_2D(grid, init, goal, cost))
