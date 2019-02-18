import numpy as np
import cv2
import argparse
import logging
import vision_pipeline
import constants

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

dim = (7, 7)
gray = None
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((dim[0] * dim[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:dim[0], 0:dim[1]].T.reshape(-1, 2)


# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

cap = cv2.VideoCapture(0)

print("Initialized camera capture stream")

while len(imgpoints) < 20:
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    cv2.imshow("cam", gray)
    cv2.waitKey(1000 // 30)
    ret, corners = cv2.findChessboardCorners(gray, dim, None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv2.drawChessboardCorners(img, dim, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)
        print("Stored a point")

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

cv2.destroyAllWindows()

vision_pipeline.save_calibration_results(mtx, dist, rvecs, tvecs, constants.CALIBRATION_FILE_LOCATION)

print("Finished calibrating")
print("Camera matrix: ")
print(str(mtx))
print("Distortion coeffs:")
print(str(dist))
