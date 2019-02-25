import atexit

import vision_pipeline
import cv2
import numpy as np
import socket
import constants
import math

def generate_socket_msg(x, y, angle):
    return bytes(str(x), 'utf-8') + b',' + \
           bytes(str(y), 'utf-8') + b',' + \
           bytes(str(angle), 'utf-8') + b'\n'


# TODO: Store calib_fname in environment variable or something
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_EXPOSURE, -6)
vision_pipeline = vision_pipeline.VisionPipeline(calib_fname=constants.CALIBRATION_FILE_LOCATION)

def exit():
    cv2.destroyAllWindows()
    cap.release()

atexit.register(exit)

while True:
    # Read image from camera
    #image = cv2.imread("test_img.jpg")

    _, image = cap.read()

    #cv2.imshow("cam", image)

    # Invert image (assuming that tapes are black and background is white)
    # TODO: Remove inversion
    #image = cv2.bitwise_not(image)
    #cv2.imshow("img", image)

    # Process image
    contours, corners_subpixel, rvecs, tvecs, dist, euler_angles = vision_pipeline.process_image(image)

    contours_img = cv2.drawContours(image, contours, -1, (0, 255, 0), thickness=3)
    #cv2.imshow("contours", contours_img)

    center = np.array([
        [0, 0, 0],
    ], dtype=np.float32)

    if rvecs is not None:
        imagePoints, jacobian = cv2.projectPoints(center, rvecs, tvecs, vision_pipeline.calibration_info.camera_matrix,
                                                  vision_pipeline.calibration_info.dist_coeffs)
        imagePoints = imagePoints.reshape(-1, 2)
        image = cv2.drawFrameAxes(image, vision_pipeline.calibration_info.camera_matrix,
                                  vision_pipeline.calibration_info.dist_coeffs,
                                  rvecs, tvecs, 1)

        corner_img = cv2.circle(image, tuple(imagePoints[0].astype(np.int32)), 3, (66, 244, 113), thickness=3)

        #if dist > 10:
        cv2.imshow("corner_img", corner_img)

        # print(euler_angles) g
            #print("dist: {0:0.2f} | angle (degrees): {1:0.2f}".format(dist, euler_angles[1]*180/math.pi))

    cv2.waitKey(1000 // 30)