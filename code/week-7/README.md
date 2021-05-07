# Week 7 - Hybrid A* Algorithm & Trajectory Generation



본 과제에서 구현해야 하는 함수는 expand함수, search함수 theta_to_stack_num함수, heuristic함수입니다.

따라서 앞에서부터 차차 구현해 보겠습니다.



## heuristic



우선 heuristic함수는 단순히 현재 위치에서 goal까지의 거리를 return해주는 함수입니다.

![image](https://user-images.githubusercontent.com/12128784/117487905-a7d33200-afa6-11eb-94c2-285895ba239c.png)





## expand

expand함수는 우선 현재 state의 속도와 각도가 주어지고 그 다음 어떠한 행동을 할지가 주어졌을 때 다음 행동을 구하는 역할입니다.

따라서 이를 구하기 위하여 속도와 각도의 변화량 그리고 위치의 변화량을 각각 계산하여 next_state로 return 해줍니다.

![image](https://user-images.githubusercontent.com/12128784/117487505-21b6eb80-afa6-11eb-9bb8-e24abce2db7d.png)





## theta_to_stack_num

theta_to_stack_num함수는 주어진 각도를 NUM_THETA_CELL(theta의 cell의 개수)에서 몇번째 index인지를 반환하는 함수입니다.

![image](https://user-images.githubusercontent.com/12128784/117488322-3a73d100-afa7-11eb-8921-c3da06ce383d.png)

## search

search함수는 목표지점에까지의 경로를 도출하는 함수입니다(단 이 때 목표지점에 도달할 수 있는 경로를 찾지 못하면 False를 반환)

![image](https://user-images.githubusercontent.com/12128784/117488961-f3d2a680-afa7-11eb-845a-1a53a75cf501.png)



경로를 탐색하는 방법은 위 그림에서 생략된 while문 안에 구현되어 있습니다.

while문 안에서 serach함수는 현재 state를 기반으로 cost가 가장 적은 쪽으로 방향을 틀고 거기로 부터 다시 다음 state로의방향을 계산합니다. 그리고 기 과정을 계속 반복하게 됩니다. 그리고 여기서 next state를 구하기 위해 사용되는것이 expand함수입니다.



![image](https://user-images.githubusercontent.com/12128784/117489367-8115fb00-afa8-11eb-8d99-c75ce0e09b34.png)





## results

위와 같은 알고리즘을 수행하면 다음과 같은 결과가 나옵니다.



![image](https://user-images.githubusercontent.com/12128784/117487447-106ddf00-afa6-11eb-953c-cf41faea8c98.png)



# Origianl

## Assignment: Hybrid A* Algorithm

In directory [`./hybrid_a_star`](./hybrid_a_star), a simple test program for the hybrid A* algorithm is provided. Run the following command to test:

```
$ python main.py
```

The program consists of three modules:

* `main.py` defines the map, start configuration and end configuration. It instantiates a `HybridAStar` object and calls the search method to generate a motion plan.
* `hybrid_astar.py` implements the algorithm.
* `plot.py` provides an OpenCV-based visualization for the purpose of result monitoring.

You have to implement the following sections of code for the assignment:

* Trajectory generation: in the method `HybridAStar.expand()`, a simple one-point trajectory shall be generated based on a basic bicycle model. This is going to be used in expanding 3-D grid cells in the algorithm's search operation.
* Hybrid A* search algorithm: in the method `HybridAStar.search()`, after expanding the states reachable from the current configuration, the algorithm must process each state (i.e., determine the grid cell, check its validity, close the visited cell, and record the path. You will have to write code in the `for n in next_states:` loop.
* Discretization of heading: in the method `HybridAStar.theta_to_stack_num()`, you will write code to map the vehicle's orientation (theta) to a finite set of stack indices.
* Heuristic function: in the method `HybridAStar.heuristic()`, you define a heuristic function that will be used in determining the priority of grid cells to be expanded. For instance, the distance to the goal is a reasonable estimate of each cell's cost.

You are invited to tweak various parameters including the number of stacks (heading discretization granularity) and the vehicle's velocity. It will also be interesting to adjust the grid granularity of the map. The following figure illustrates an example output of the program with the default map given in `main.py` and `NUM_THETA_CELLS = 360` while the vehicle speed is set to 0.5.

![Example Output of the Hybrid A* Test Program][has-example]

---

## Experiment: Polynomial Trajectory Generation

In directory [`./PTG`](./PTG), a sample program is provided that tests polynomial trajectory generation. If you input the following command:

```
$ python evaluate_ptg.py
```

you will see an output such as the following figure.

![Example Output of the Polynomial Trajectory Generator][ptg-example]

Note that the above figure is an example, while the result you get will be different from run to run because of the program's random nature. The program generates a number of perturbed goal configurations, computes a jerk minimizing trajectory for each goal position, and then selects the one with the minimum cost as defined by the cost functions and their combination.

Your job in this experiment is:

1. to understand the polynomial trajectory generation by reading the code already implemented and in place; given a start configuration and a goal configuration, the algorithm computes coefficient values for a quintic polynomial that defines the jerk minimizing trajectory; and
2. to derive an appropriate set of weights applied to the cost functions; the mechanism to calculate the cost for a trajectory and selecting one with the minimum cost is the same as described in the previous (Week 6) lecture.

Experiment by tweaking the relative weight for each cost function. It will also be very interesting to define your own cost metric and implement it using the information associated with trajectories.
