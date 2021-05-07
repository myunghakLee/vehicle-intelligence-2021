import numpy as np
import random
from math import sqrt, pi, exp

def gaussian_prob(obs, mu, sig):
    # Calculate Gaussian probability given
    # - observation
    # - mean
    # - standard deviation
    num = (obs - mu) ** 2
    denum = 2 * sig ** 2
    norm = 1 / sqrt(2 * pi * sig ** 2)
    return norm * exp(-num / denum)

# Gaussian Naive Bayes class
class GNB():
    # Initialize classification categories
    def __init__(self):
        self.behavior_class = ['left', 'keep', 'right']
        self.prior = {}
        for c in self.behavior_class:
            self.prior[c] = {}
    # Given a set of variables, preprocess them for feature engineering.
    def process_vars(self, vars):
        # The following implementation simply extracts the four raw values
        # given by the input data, i.e. s, d, s_dot, and d_dot.
        s, d, s_dot, d_dot = vars
        return s, d, s_dot, d_dot

    # Train the GNB using a combination of X and Y, where
    # X denotes the observations (here we have four variables for each) and
    # Y denotes the corresponding labels ("left", "keep", "right").
    def train(self, X, Y):
        '''
        Collect the data and calculate mean and standard variation
        for each class. Record them for later use in prediction.
        '''
        # TODO: implement code.
        X_ = [
            {'left':[], 'keep':[], 'right':[]},
            {'left':[], 'keep':[], 'right':[]},
            {'left':[], 'keep':[], 'right':[]},
            {'left':[], 'keep':[], 'right':[]}
        ]
        for x, y in zip(X, Y):
            for i in range(len(X_)):
                X_[i][y].append(self.process_vars(x)[i])

        xn = ['x1','x2','x3','x4']
        for i, k1 in enumerate(sorted(self.prior.keys())):
            for k2, x_ in zip(xn, X_):
                self.prior[k1][k2] = [np.mean(x_[k1]), np.std(x_[k1])]

    # Given an observation (s, s_dot, d, d_dot), predict which behaviour
    # the vehicle is going to take using GNB.
    def predict(self, observation):
        '''
        Calculate Gaussian probability for each variable based on the
        mean and standard deviation calculated in the training process.
        Multiply all the probabilities for variables, and then
        normalize them to get conditional probabilities.
        Return the label for the highest conditional probability.
        '''
        # TODO: implement code.
        best = -9999999
        best_idx = 0

        for i, c in enumerate(self.behavior_class) :
            p = 1
            for o, xn in zip(observation, ['x1','x2','x3','x4']):
                p*= gaussian_prob(o, self.prior[c][xn][0], self.prior[c][xn][1])

            if best < p:
                best_idx = i
                best = p

        return self.behavior_class[best_idx]
