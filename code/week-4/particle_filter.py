import copy
import numpy as np
from helpers import distance

class ParticleFilter:
    def __init__(self, num_particles):
        self.initialized = False
        self.num_particles = num_particles

    # Set the number of particles.
    # Initialize all the particles to the initial position
    #   (based on esimates of x, y, theta and their uncertainties from GPS)
    #   and all weights to 1.0.
    # Add Gaussian noise to each particle.
    def initialize(self, x, y, theta, std_x, std_y, std_theta):
        self.particles = []
        for i in range(self.num_particles):
            self.particles.append({
                'x': np.random.normal(x, std_x),
                'y': np.random.normal(y, std_y),
                't': np.random.normal(theta, std_theta),
                'w': 1.0,
                'assoc': [],
            })
        self.initialized = True

    # Add measurements to each particle and add random Gaussian noise.
    def predict(self, dt, velocity, yawrate, std_x, std_y, std_theta):
        # Be careful not to divide by zero.
        v_yr = velocity / yawrate if yawrate else 0
        yr_dt = yawrate * dt
        for p in self.particles:
            # We have to take care of very small yaw rates;
            #   apply formula for constant yaw.
            if np.fabs(yawrate) < 0.0001:
                xf = p['x'] + velocity * dt * np.cos(p['t'])
                yf = p['y'] + velocity * dt * np.sin(p['t'])
                tf = p['t']
            # Nonzero yaw rate - apply integrated formula.
            else:
                xf = p['x'] + v_yr * (np.sin(p['t'] + yr_dt) - np.sin(p['t']))
                yf = p['y'] + v_yr * (np.cos(p['t']) - np.cos(p['t'] + yr_dt))
                tf = p['t'] + yr_dt
            p['x'] = np.random.normal(xf, std_x)
            p['y'] = np.random.normal(yf, std_y)
            p['t'] = np.random.normal(tf, std_theta)

    # Find the predicted measurement that is closest to each observed
    #   measurement and assign the observed measurement to this
    #   particular landmark.
    def associate(self, predicted, observations):
        associations = []
        # For each observation, find the nearest landmark and associate it.
        #   You might want to devise and implement a more efficient algorithm.
        for o in observations:
            min_dist = -1.0
            for p in predicted:
                dist = distance(o, p)
                if min_dist < 0.0 or dist < min_dist:
                    min_dist = dist
                    min_id = p['id']
                    min_x = p['x']
                    min_y = p['y']
            association = {
                'id': min_id,
                'x': min_x,
                'y': min_y,
            }
            associations.append(association)
        # Return a list of associated landmarks that corresponds to
        #   the list of (coordinates transformed) predictions.
        return associations

    # Update the weights of each particle using a multi-variate
    #   Gaussian distribution.
    def update_weights(self, sensor_range, std_landmark_x, std_landmark_y,
                       observations, map_landmarks): # self.particle의 w값을 바꾸자!!!
        calc_dist = lambda A,B: ((A[0] - B[0]) ** 2 + (A[1] - B[1]) **2) ** 0.5
        norm_pdf = lambda x, m, s: (1 / ((2 * np.pi)**0.5) / s) * np.exp(-(((x - m) / s) ** 2) /2) # exp에 절대값이 너무 큰 음수를 제곱하면 0이 되버림

        for p in self.particles:
            landmarks = []
            absolute_cord_obs = []

            for k in map_landmarks.keys():
                x,y = map_landmarks[k]["x"], map_landmarks[k]["y"] 
                if calc_dist([x,y], [p["x"], p["y"]]) < sensor_range:
                    landmarks.append({"id": k, "x" : x, "y" : y})
            # if len(landmarks) == 0:
            #     print(len(self.particles))
            #     continue

            transfoer_matrix = [[np.cos(p['t']), -np.sin(p['t'])],
                                [np.sin(p['t']),  np.cos(p['t'])]]
            for o in observations:
                x= p['x'] + np.dot([o['x'],o['y']], transfoer_matrix[0])
                y= p['y'] + np.dot([o['x'],o['y']], transfoer_matrix[1])
                absolute_cord_obs.append({'x': x, 'y': y})




            all_associates = self.associate(landmarks, absolute_cord_obs)

            p['w'] = 1.0
            p['assoc'] = []
            
            for i, assoc in enumerate(all_associates):
                p['w'] *= norm_pdf(calc_dist((assoc['x'], assoc['y']), (p['x'], p['y'])),
                                        (observations[i]['x']**2 + observations[i]['y'] **2) ** 0.5,
                                        (std_landmark_x**2 + std_landmark_y**2)**0.5)
                p['w'] += 0.0 if p['w'] != 0 else 0.00000000000000000001


                p['assoc'].append(assoc['id'])    


    # Resample particles with replacement with probability proportional to
    #   their weights.
    def resample(self):
        # resample_p = []
        # sum_particles = sum([i['w'] for i in self.particles])


        particles_prob = np.array([i['w'] for i in self.particles])
        particles_prob /= np.sum(particles_prob)
        random_idx = np.random.choice(self.num_particles, self.num_particles, p=particles_prob)
        self.particles = [copy.deepcopy(self.particles[i]) for i in random_idx ]

        # self.particles = resample_p
    # Choose the particle with the highest weight (probability)
    def get_best_particle(self):
        highest_weight = -1.000000000000000000000000000
        try:
            # print(len(self.particles))
            for p in self.particles:
                if p['w'] > highest_weight:
                    highest_weight = p['w']
                    best_particle = p

            return best_particle
        except:
            print(self.particles)
            exit(True)