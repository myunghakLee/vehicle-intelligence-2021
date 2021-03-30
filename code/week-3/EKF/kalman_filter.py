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
        def H(z):
            x,y,vx,vy = z
            return np.array([np.sqrt(x**2 + y**2),
                             np.tanh(y/x),
                             (x*vx + y*vy)/np.sqrt(x**2 +y**2)
                            ])
        # z: rho, phi, 'rho_dot'
        rho, phi, rho_dot = z  # x'

        px, py = rho * np.cos(phi), rho * np.sin(phi)
        vx,vy = rho_dot * np.cos(phi), rho_dot * np.sin(phi)

        H_j = Jacobian([px,py,vx,vy])

        y = z - H(self.x)
        S = H_j.dot(self.P).dot(H_j.T) + self.R
        K = self.P.dot(H_j.T).dot(np.linalg.inv(S))
        x = self.x + K.dot(y)

        I = np.array([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [0,0,0,1]])

        P = (I-K.dot(H_j)).dot(self.P)

        return 1

        
        # TODO: Implement EKF update for radar measurements
        # 1. Compute Jacobian Matrix H_j
        # 2. Calculate S = H_j * P' * H_j^T + R
        # 3. Calculate Kalman gain K = H_j * P' * Hj^T + R

        # 4. Estimate y = z - h(x')
        # 5. Normalize phi so that it is between -PI and +PI
        # 6. Calculate new estimates
        #    x = x' + K * y
        #    P = (I - K * H_j) * P
