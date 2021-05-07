# Week 5 - Path Planning & the A* Algorithm

---

본 과제는 A*algorithm을 통해 경로를 찾아 가는 것이다. 단 이 때 left, right, forward 3가지 방향이 있고 각 방향마다 cost가 존재한다는 것이다.

따라서 현재 위치로 부터 갈 수 있는 방향(왼쪽, 오른쪽, 직진) 에 각 cost에 해당하는 값을 적어준다. 단 이 때 미리 적혀있는 값보다 작은 경우만 값을 바꾸어 준다.

위 과정을 우리는 계속 반복하게 된다.

단 기존의 A* 알고리즘과 다르게 도착점에 도달하였다고 알고리즘을 끝내지 않는다. 알고리즘이 끝나는 조건은 더이상 변하는 값이 없는 경우이다.

























# Original

## Examples

We have four small working examples for demonstration of basic path planning algorithms:

* `search.py`: simple shortest path search algorithm based on BFS (breadth first search) - only calculating the cost.
* `path.py`: built on top of the above, generating an optimum (in terms of action steps) path plan.
* `astar.py`: basic implementation of the A* algorithm that employs a heuristic function in expanding the search.
* `policy.py`: computation of the shortest path based on a dynamic programming technique.

These sample source can be run as they are. Explanation and test results are given in the lecture notes.

## Assignment

You will complete the implementation of a simple path planning algorithm based on the dynamic programming technique demonstrated in `policy.py`. A template code is given by `assignment.py`.

The assignmemt extends `policy.py` in two aspects:

* State space: since we now consider not only the position of the vehicle but also its orientation, the state is now represented in 3D instead of 2D.
* Cost function: we define different cost for different actions. They are:
	- Turn right and move forward
	- Move forward
	- Turn left and move forward

This example is intended to illustrate the algorithm's capability of generating an alternative (detouring) path when left turns are penalized by a higher cost than the other two possible actions. When run with the settings defined in `assignment.py` without modification, a successful implementation shall generate the following output,

```
[[' ', ' ', ' ', 'R', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', '#'],
 ['*', '#', '#', '#', '#', 'R'],
 [' ', ' ', ' ', '#', ' ', ' '],
 [' ', ' ', ' ', '#', ' ', ' ']]
```

because of the prohibitively high cost associated with a left turn.

You are highly encouraged to experiment with different (more complex) maps and different cost settings for each type of action.
