import cv2
import numpy as np
from KalmanFilter import KalmanFilter
import imutils


def main():

	# Create opencv video capture object
	VideoCap = cv2.VideoCapture(2)

	#Variable used to control the speed of reading the video
	ControlSpeedVar = 10 #Lowest: 1 - Highest:100

	HiSpeed = 100

	#Create KalmanFilter object KF
	#KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)

	KF = KalmanFilter(0.1, 1, 1, 1, 0.1,0.1)

	while(True):
		# Read frame
		ret, frame = VideoCap.read()

		# Detect object
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		lower = np.array([0, 102, 128])
		upper = np.array([61, 205, 249])
		mask = cv2.inRange(hsv, lower, upper)

		contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)
		center=[]
		for c in contours:
			M = cv2.moments(c)
			if M['m00'] != 0:
				cx = int(M['m10'] / M['m00'])
				cy = int(M['m01'] / M['m00'])
			# else:
			# 	cx, cy = 0,0
				center.append(np.array([[cx], [cy]]))

		# If centroids are detected then track them
		if (len(center) > 0):

			# Draw the detected circle
			cv2.circle(frame, (int(center[0][0]), int(center[0][1])), 10, (0, 191, 255), 15)

			# Predict
			cx, cy = KF.predict()
			# Draw a rectangle as the predicted object position
			cv2.rectangle(frame, (int(cx - 15), int(cy - 15)), (int(cx + 15), int(cy + 15)), (255, 0, 0), 15)

			# Update
			cx1, cy1 = KF.update(center[0])
			# print(center[0])

			# Draw a rectangle as the estimated object position
			# cv2.rectangle(frame, (int(cx1 - 15), int(cy1 - 15)), (int(cx1 + 15), int(cy1 + 15)), (0, 0, 255), 15)

			#cv2.putText(frame, "Estimated Position", (int(x1 + 15), int(y1 + 10)), 0, 0.5, (0, 0, 255), 2)
			print("Estimated Position: ", (int(cx1 + 15), int(cy1 + 10)))
			#cv2.putText(frame, "Predicted Position", (int(x + 15), int(y)), 0, 0.5, (255, 0, 0), 2)
			# print("Predicted Position: ", (int(cx + 15), int(cy)))
			#cv2.putText(frame, "Measured Position", (int(centers[0][0] + 15), int(centers[0][1] - 15)), 0, 0.5, (0,191,255), 2)
			print("Measured Position: ", (int(center[0][0] + 15), int(center[0][1] - 15)))
		
		imgResize = cv2.resize(frame, (0, 0), None, 0.3, 0.3)
		cv2.imshow('image', imgResize)
	

		if cv2.waitKey(2) & 0xFF == ord('q'):
			VideoCap.release()
			cv2.destroyAllWindows()
			break

		cv2.waitKey(HiSpeed-ControlSpeedVar+1)


if __name__ == "__main__":
	# execute main
	main()
