from Kalman import KalmanFilter
import cv2

# Kalman Filter

img = cv2.imread("item.png")

ball1_positions = [(100, 200), (100, 120), (124, 250), (140, 250), (165, 255), (180, 245), (190, 255), (195, 250), (200, 250)]

ball2_positions = [(4, 300), (61, 256), (116, 214), (170, 180), (225, 148), (279, 120), (332, 97),
         (383, 80), (434, 66), (484, 55), (535, 49), (586, 49), (634, 50),
         (683, 58), (731, 69), (778, 82), (824, 101), (870, 124), (917, 148),
         (962, 169), (1006, 212), (1051, 249), (1093, 290)]

for pt in ball2_positions:
    kf = KalmanFilter(0.1, pt[0], pt[1], 1, 0.1, 0.1)
    # print("as",pt[0],pt[1])
    cv2.circle(img, pt, 15, (0, 20, 220), -1)
    # predicted = kf.predict()
    # print(predicted)
    # update = kf.update(predicted)
    # print(update)

for i in range(20):
    predicted = kf.predict()
    update = kf.update(predicted)
    if (i % 5 == 0):
        cv2.circle(img, (int(predicted[0]), int(predicted[1])), 15, (20, 220, 0), 4)
        print("as",pt[0],pt[1])

        print(predicted)
        print(update)


cv2.imshow("item", img)
cv2.waitKey(0)