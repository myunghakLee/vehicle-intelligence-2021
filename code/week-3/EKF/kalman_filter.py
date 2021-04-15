import numpy as np
from math import sqrt
from math import atan2
from tools import Jacobian

class KalmanFilter:
    def __init__(self, x_in, P_in, F_in, H_in, R_in, Q_in):
        self.x = x_in
        self.P = P_in
        self.F = F_in
        self.H = H_in
        self.R = R_in
        self.Q = Q_in

    def predict(self):
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q

    def update(self, z):
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
        # Calculate new estimates
        self.x = self.x + np.dot(K, z - np.dot(self.H, self.x))
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)

    def update_ekf(self, z): 
        def H(px, py, vx, vy):
            return np.array([np.sqrt(px**2 + py**2),
                             np.arctan(py/px) + (0 if (px>=0) else (np.pi * ((py>=0)*2-1))),
                             (px*vx + py*vy)/np.sqrt(px**2 +py**2)
                            ])
        
        px, py, vx, vy = self.x

        y = z - H(px, py, vx, vy)
        y[1] = y[1] % -np.pi if y[1] < 0 else y[1] % np.pi        


        H_j = Jacobian(self.x)
        S = H_j.dot(self.P).dot(H_j.T) + self.R
        K = self.P.dot(H_j.T).dot(np.linalg.inv(S))


        self.x += np.dot(K, y)
        self.P -= np.dot(np.dot(K, H_j), self.P)

