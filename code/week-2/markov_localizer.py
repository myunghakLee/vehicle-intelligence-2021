from helper import norm_pdf
import numpy as np

# Initialize prior probabilities
# taking into account that the vehicle is initially parked
# around one of the landmarks and we do not know which.
def initialize_priors(map_size, landmarks, stdev):
    # Set all probabilities to zero initially.
    priors = [0.0] * map_size
    # Initialize prior distribution assuming the vehicle is at
    # landmark +/- 1.0 meters * stdev.
    positions = []
    for p in landmarks:
        start = int(p - stdev) - 1
        if start < p:
            start += 1
        c = 0
        while start + c <= p + stdev:
            # Gather positions to set initial probability.
            positions.append(start + c)
            c += 1
    # Calculate actual probability to be uniformly distributed.
    prob = 1.0 / len(positions)
    # Set the probability to each position.
    for p in positions:
        priors[p] += prob
    return priors

# Estimate pseudo range determined according to the
# given pseudo position.
def estimate_pseudo_range(landmarks, p):
    pseudo_ranges = []
    # Loop over each landmark and estimate pseudo ranges
    for landmark in landmarks:
        dist = landmark - p
        # Consider only those landmarks ahead of the vehicle.
        if dist > 0:
            pseudo_ranges.append(dist)
    return pseudo_ranges

# Motion model (assuming 1-D Gaussian dist)
def motion_model(position, mov, priors, map_size, stdev): # 내 움직임에 의해 belief가 약해짐
    # Initialize the position's probability to zero.

    # position에 있을 확률을 구해라
    # 내속도는 mov다
    # 분산은 stdev다


    
    position_prob = 0.0
    for i in range(len(priors)): #  position - i만큼 움직였을 확률을 구하자.
        x = position - i
        position_prob += priors[i] * (1 / np.sqrt(2 * np.pi)) * np.exp(- ((x - 1) ** 2) / 2 * (stdev ** 2) )



    # 평균이 mov 분산이 stdev인 위치에 정규분포표를 그려라
    # 내가 움직인 거리는 평균이 mov, 분산이 stdev만큼이다.
    # print("priors", priors)  [0,0,0,0,0,0,...]



    # TODO: Loop over state space for all possible prior positions,
    # calculate the probability (using norm_pdf) of the vehicle
    # moving to the current position from that prior.
    # Multiply this probability to the prior probability of
    # the vehicle "was" at that prior position.
    return position_prob

# Observation model (assuming independent Gaussian)
def observation_model(landmarks, observations, pseudo_ranges, stdev): # 내 관측임에 의해 belief가 강해짐
    # Initialize the measurement's probability to one.
    # 평균은 pseudo, 표준편차는 stdev

    distance_prob = 1.0
    print("observations: ", observations)
    print("pseudo_ranges: ", pseudo_ranges)
    print("=" * 100)


    if len(observations) == 0:
        return 0
    elif len(observations)>len(pseudo_ranges):
        return 0
    else:
        for i in range(len(observations)): # 평균이 pseudo_ranges이고 분산이 stdev일때 observation[j]일 확률
            x = pseudo_ranges[i] - observations[i]
            distance_prob *=  (1 / np.sqrt(2 * np.pi)) * np.exp(- ((x) ** 2) / 2 * (stdev ** 2) )



    # print("landmarks: ", landmarks)

    # TODO: Calculate the observation model probability as follows:
    # (1) If we have no observations, we do not have any probability.
    # (2) Having more observations than the pseudo range indicates that
    #     this observation is not possible at all.
    # (3) Otherwise, the probability of this "observation" is the product of
    #     probability of observing each landmark at that distance, where
    #     that probability follows N(d, mu, sig) with
    #     d: observation distance
    #     mu: expected mean distance, given by pseudo_ranges
    #     sig: squared standard deviation of measurement
    print("distance_prob: ", distance_prob)
    return distance_prob

# Normalize a probability distribution so that the sum equals 1.0.
def normalize_distribution(prob_dist):
    normalized = [0.0] * len(prob_dist)
    total = sum(prob_dist)
    for i in range(len(prob_dist)):
        if (total != 0.0):
            normalized[i] = prob_dist[i] / total
    return normalized
