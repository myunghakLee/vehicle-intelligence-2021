import matplotlib.pyplot as plt
import matplotlib.animation as animation
from helper import GraphAnimator

from markov_localizer import initialize_priors
from markov_localizer import estimate_pseudo_range
from markov_localizer import motion_model
from markov_localizer import observation_model
from markov_localizer import normalize_distribution

'''
한 time-step마다 1m씩 움직인다(단 noise가 없으면).
처음에 tree 옆에 차가 있다는 것만 알고 어느 tree인지 모름
센서는 내 앞에 나무들까지의 거리만 알 수 있음(일정 거리까지만, 즉 안보이는것도 있을 수 있음)
'''


if __name__ == '__main__':
    # Initialize graph data to an empty list
    graph = []
    # Std dev for initial position
    position_stdev = 1.0
    # Std dev for control (movement)
    control_stdev = 1.0
    # Std dev for observation (measurement)
    observation_stdev = 1.0
    # Assumed constant velocity of vehicle
    mov_per_timestep = 1.0

    # Size of the map
    map_size = 25
    # Map (landmark positions)
    landmark_positions = [3, 9, 14, 23]

    # Observation data
    observations = [

        [1, 7, 12, 21],
        [0, 6, 11, 20],
        [5, 10, 19],
        [4, 9, 18],
        [3, 8, 17],
        [2, 7, 16],
        [1, 6, 15],
        [0, 5, 14],
        [4, 13],
        [3, 12],
        [2, 11],
        [1, 10],
        [0, 9],
        [8],
        [7],
        [6],
        [5],
        [4],
        [3],
        [2],
        [1],
        [0],
        [],
        [],
        [],
    ]

    # Initialize priors (initial belief)
    priors = initialize_priors(
        map_size, landmark_positions, position_stdev
    )
    # Cycle through timesteps
    for t in range(len(observations)):
        '''
        print("---------------TIME STEP---------------")
        print("t = %d" % t)
        print("-----Motion----------OBS----------------PRODUCT--")
        '''
        posteriors = [0.0] * map_size   # 각 위치에 있을 확률 초기화

        # for l in landmark_positions:
        #     posterios[min(max(0,l-1), len(landmark_positions)-1)] = 1/len(landmark_positions)/3
        #     posterios[min(max(0,l), len(landmark_positions)-1)] = 1/len(landmark_positions)/3
        #     posterios[min(max(0,l+1), len(landmark_positions)-1)] = 1/len(landmark_positions)/3




        # Step through each pseudo position p (to determine pdf)
        for pseudo_position in range(map_size):
            # Prediction:
            # Calculate probability of the vehicle being at position p
            motion_prob = motion_model(
                pseudo_position, mov_per_timestep, priors,
                map_size, control_stdev
            )

            # Get pseudo range
            pseudo_ranges = estimate_pseudo_range(
                landmark_positions, pseudo_position
            )
            print("pseudo_position: ", pseudo_position)
            # Measurement update:
            # Calculate observation probability
            observation_prob = observation_model(
                landmark_positions, observations[t],
                pseudo_ranges, observation_stdev
            )
            # Calculate posterior probability
            # print("pseudo_ranges : ", pseudo_ranges)
            # print("pseudo_position : ", pseudo_position)
            # print("observation_prob : ", observation_prob)
            
            posteriors[pseudo_position] = motion_prob * observation_prob

            '''
            print("%f\t%f\t%f" % (motion_prob,
                                  observation_prob,
                                  posteriors[pseudo_position])
            )
            '''
        # Normalize the posterior probability distribution

        print("posteriors : ", posteriors)
        posteriors = normalize_distribution(posteriors)
        # Update priors with posteriors
        priors = posteriors
        # Collect data to plot according to timestep.
        graph.append(posteriors)

    # Now we generate an animated plot with the saved data.
    fig, ax = plt.subplots(figsize=(10, 10), num='Markov Localization')
    bgraph = plt.bar(range(map_size), [0] * map_size)
    plt.ylim(0, 1)
    graph_animator = GraphAnimator(bgraph, graph)
    ani = animation.FuncAnimation(
        fig, graph_animator.animate, blit=True, interval=1000, repeat=False,
        frames=len(graph)
    )
    plt.show()

