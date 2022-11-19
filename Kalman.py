import numpy as np

class KalmanFilter(object):
    def __init__(self, dt, x, y, sX, sY, std_acc, x_std_meas, y_std_meas):
        self.dt = dt

        #Initial percepatan
        self.a = np.matrix([[sX],[sY]])

        #Initial posisi dan kecepatan
        self.i = np.matrix([[x],[y],[sX],[sY]])

        # Define the State Transition Matrix V
        self.V = np.matrix([[1, 0, self.dt, 0],
                            [0, 1, 0, self.dt],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        # Define the Control Input Matrix Z    
        self.Z = np.matrix([[0,(self.dt**2)/2],
                            [(self.dt**2)/2,0],
                            [self.dt,0],
                            [0,self.dt]])

        # Define Measurement Mapping Matrix
        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0]])

        #Initial Process Noise Covariance
        self.Q = np.matrix([[(self.dt**4)/4, 0, (self.dt**3)/2, 0],
                            [0, (self.dt**4)/4, 0, (self.dt**3)/2],
                            [(self.dt**3)/2, 0, self.dt**2, 0],
                            [0, (self.dt**3)/2, 0, self.dt**2]]) * std_acc**2

        #Initial Measurement Noise Covariance
        self.R = np.matrix([[x_std_meas**2,0],
                           [0, y_std_meas**2]])

        #Initial Covariance Matrix
        self.P = np.eye(self.V.shape[1])
    
    def predict(self):

        self.n = np.dot(self.V, self.i) + np.dot(self.Z, self.a)
        self.P = np.dot(np.dot(self.V, self.P), self.V.T) + self.Q

        return self.n[0:2]

    def update(self, z):

        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        self.n = np.round(self.n + np.dot(K, (z - np.dot(self.H, self.n))))

        I = np.eye(self.H.shape[1])

        self.P = (I - (K * self.H)) * self.P 
        return self.n[0:2]





