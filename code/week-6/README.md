# Week 6 - Prediction & Behaviour Planning

## BP(Behavior Planning)

여기서 우리가 해야할 일은 cost function을 작성하는 부분과 vehicle파일 안의 cost function을 통해 계산된 cost를 이용해 최적의 행동을 선택하는 함수입니다. 

이 때 저는 cost function을 다음과 같이 짰습니다. 우선 처음에는 goal_distnace_cost를 낮추고 그 뒤에는 점점 높아지게 하기 위하여 num_lane_to_goal에서 distance_to_goal을 나누어 주었고 이 효과를 좀더 극대화 하기 위하여 distance_to_goal을 제곱해 주었으며 이 때 distance_to_goal이 너무 커지지 않게 하기 위하여 10을 나눔으로 인하여 normalize하였습니다.

![image](https://user-images.githubusercontent.com/12128784/117484934-b3245e80-afa2-11eb-82fc-147e75896efd.png)









또한 inefficiency_cost에도 도착점까지의 거리를 변수로 넣어줄까도 생각하였지만 이는 이미 goal_distance_cost함수에 들어가 있고 이것으로 충분하다고 생각하다여 생략하였습니다.

그대신 단순히 최대 속도에서의 차이를 최대 속도로 normalize한 값만큼을 cost로 사용하였습니다.

![image](https://user-images.githubusercontent.com/12128784/117485394-478ec100-afa3-11eb-9b19-614c1b196128.png)





## GNB(Gaussian Naive Bayes)

여기서는 trian data(action data: left, keep, right)의 평균과 분산을 구합니다.

![image](https://user-images.githubusercontent.com/12128784/117486187-4ad67c80-afa4-11eb-8c3e-aa3b68e620af.png)



그 후 test에서는 train data를 가지고 구한 평균과 분산을 가지고 각 action에 대한 확률을 구하고 이 중 가장 높은 값을 갖는 action을 선택합니다. 



![image](https://user-images.githubusercontent.com/12128784/117486249-5d50b600-afa4-11eb-8c5c-500a418257bb.png)

단 이 때 만약 각 행동마다 확률이 다르다면(즉 왼쪽으로 갈 확률과 오른쪽으로 갈 확률이 다르다면) 이 값에 맞추어 p를 normalize해야하지만 본 과제는 모두 같다는 것을 가정하였으므로 무시하였습니다.



# origianl

## Assignment #1

Under the directory [./GNB](./GNB), you are given two Python modules:

* `prediction.py`: the main module you run. The `main()` function does two things: (1) read an input file ([`train.json`](./GNB/train.json)) and train the GNB (Gaussian Naive Bayes) classifier using the data stored in it, and (2) read another input file ([`test.json`](./GNB/test.json)) and make predictions for a number of data points. The accuracy measure is taken and displayed.
* `classifier.py`: main implementation of the GNB classifier. You shall implement two methods (`train()` and `precict()`), which are used to train the classifier and make predictions, respectively.

Both input files ([`train.json`](./GNB/train.json) and [`test.json`](./GNB/test.json)) have the same format, which is a JSON-encoded representation of training data set and test data set, respectively. The format is shown below:

```
{
	"states": [[s_1, d_1, s_dot_1, d_dot_1],
	           [s_2, d_2, s_dot_2, d_dot_2],
	           ...
	           [s_n, d_n, s_dot_n, d_dot_n]
	          ],
	"labels": [L_1, L_2, ..., L_n]
}
```

The array `"states"` have a total of `n` items, each of which gives a (hypothetically) measured state of a vehicle, where `s_i` and `d_i` denote its position in the Frenet coordinate system. In addition, `s_dot_i` and `d_dot_i` give their first derivates, respectively. For each measured state, a label is associated (given in the `"labels"` array) that represents the vehicle's behaviour. The label is one of `"keep"`, `"left"`, and `"right"`, which denote keeping the current lane, making a left turn, and making a right turn, respectively.

The training set has a total of 750 data points, whereas the test set contains 250 data points with the ground truth contained in `"labels"`.

The GNB classifier is trained by computing the mean and variance of each component in the state variable for each observed behaviour. Later it is used to predict the behaviour by computing the Gaussian probability of an observed state for each behaviour and taking the maximum. You are going to implement that functionality. For convcenience, a separate function `gaussian_prob()` is already given in the module `classifier.py`.


---

## Assignment #2

Under the directory [./BP](./BP), you are given four Python modules:

* `simulate_behavior.py`: the main module you run. It instantiates a simple text-based simulation environment and runs it using the configuration specified in the same module.
* `road.py`: `class Road` is implemented here. It captures the state of the simulated road with a number of vehicles (including the ego) running on it, and visualizes it using terminal output.
* `vehicle.py`: `class Vehicle` implements the states of a vehicle and its transition, along with the vehicle's dynamics based on a simple kinematic assumption. Note that a vehicle's trajectory is represented by two instances of object of this class, where the first one gives the current state and the second one predicts the state that the vehicle is going to be in after one timestep.
* `cost_functions.py`: implementation of cost functions governing the state transition of the ego vehicle. The main job required for your assignment is to provide an adequate combination of cost functions by implementing them in this module.

### Task 1

Implement the method `choose_next_state()` in `vehicle.py`. It should

* determine which state transitions are possible from the current state (`successor_states()` function in the same module will be helpful),
* calculate cost for each state transition using the trajectory generated for each behaviour, and
* select the minimum cost trajectory and return it.

Note that you must return a planned trajectory (as described above) instead of the state that the vehicle is going to be in.

### Task 2

In `cost_functions.py`, templates for two different cost functions (`goal_distance_cost()` and `inefficiency_cost()`) are given. They are intended to capture the cost of the trajectory in terms of

* the lateral distance of the vehicle's lane selection from the goal position, and
* the time expected to be taken to reach the goal (because of different lane speeds),

respectively.

Note that the range of cost functions should be carefully defined so that they can be combined by a weighted sum, which is done in the function `calculate_cost()` (to be used in `choose_next_state()` as described above). In computing the weighted sum, a set of weights are used. For example, `REACH_GOAL` and `EFFICIENCY` are already defined (but initialized to zero values). You are going to find out a good combination of weights by an empirical manner.

You are highly encouraged to experiment with your own additional cost functions. In implementing cost functions, a trajectory's summary (defined in `TrajectoryData` and given by `get_helper_data()`) can be useful.

You are also invited to experiment with a number of different simulation settings, especially in terms of

* number of lanes
* lane speed settings (all non-ego vehicles follow these)
* traffic density (governing the number of non-ego vehicles)

and so on.

Remember that our state machine should be geared towards reaching the goal in an *efficient* manner. Try to compare a behaviour that switches to the goal lane as soon as possible (note that the goal position is in the slowest lane in the given setting) and one that follows a faster lane and move to the goal lane as the remaining distance decreases. Observe different behaviour taken by the ego vehicle when different weights are given to different cost functions, and also when other cost metrics (additional cost functions) are used.
