import cv2
import numpy as np
from Kalman import KalmanFilter
import imutils

class Camera(object):
    def __init__(self):
        self.VideoCap = cv2.VideoCapture(0)

    def get_frame(self):
        ret, self.frame = self.VideoCap.read()
        if ret :
            pass
        return self.frame
    
    def get_contours(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        lower = np.array([0, 102, 128])
        upper = np.array([61, 205, 249])
        mask = cv2.inRange(hsv, lower, upper)
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        self.center=[]
        for c in contours:
            M = cv2.moments(c)
            if M['m00'] != 0:
                self.cx = int(M['m10'] / M['m00'])
                self.cy = int(M['m01'] / M['m00'])
                self.center.append(np.array([[self.cx], [self.cy]]))

        return self.center

    def release_camera(self):
        self.VideoCap.release()

class Filter():
    def __init__(self):
        self.coor = Camera().get_contours()
    
    def perX(self, n):
        self.coorX = self.coor[0][0]
        xPrev = 0
        sX = 0
        for i in n:
            sX[i] = self.coorX - xPrev
            xPrev = self.coorX
            return sX[i]

    def perY(self, n):
        self.coorY = self.coor[0][1]
        yPrev = 0
        sY = 0
        for i in n:
            sY[i] = self.coorX - yPrev
            yPrev = self.coorX
            return sY[i]

def main():
    while(True):
        cen = Camera().get_contours()
        cam = Camera().get_frame()
        if (len(cen)>0):
            cv2.circlecircle(cam, (int(cen[0][0]), int(cen[0][1])), 10, (0, 191, 255), 15)
            KF = KalmanFilter(0.1, int(cen[0][0]), int(cen[0][1]), 1, 0.1, 0.1)


        # imgResize = cv2.resize(cam, (0, 0), None, 0.3, 0.3)


