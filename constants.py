import os
import math
import numpy as np


def _rot_mat(rad):
    return np.array([
        [math.cos(rad), -math.sin(rad)],
        [math.sin(rad), math.cos(rad)]
    ])



# Calibration file info
BLENDER_CALIBRATION_INFO_LOCATION = "./blender_calib_info.pickle"
"""
The location of the pickled CalibrationResults that contains the calibration information for the blender camera. 
It is used for processing the autogen images.
"""

# Vision tape dimensions
VISION_TAPE_LENGTH_IN = 5.5
"""Length of the vision tape (inches)"""

VISION_TAPE_LENGTH_FT = VISION_TAPE_LENGTH_IN / 12
"""Length of the vision tape (feet)"""

VISION_TAPE_WIDTH_IN = 2
"""Width of the vision tape (inches)"""

VISION_TAPE_WIDTH_FT = 2 / 12
"""Width of the vision tape (feet)"""

# Vision tape angles
VISION_TAPE_ANGLE_FROM_VERT_DEG = 14.5
"""Angle between the vision tape and the vertical axis (degrees)"""

VISION_TAPE_ANGLE_FROM_VERT_RAD = math.radians(VISION_TAPE_ANGLE_FROM_VERT_DEG)
"""Angle between the vision tape and the vertical axis (radians)"""

VISION_TAPE_ANGLE_FROM_HORIZONTAL_DEG = 90 - VISION_TAPE_ANGLE_FROM_VERT_DEG
"""Angle between the vision tape and the horizontal axis (degrees)"""

VISION_TAPE_ANGLE_FROM_HORIZONTAL_RAD = math.radians(VISION_TAPE_ANGLE_FROM_HORIZONTAL_DEG)
"""Angle between the vision tape and the horizontal axis (radians)"""

# Vision tape relative geometry
VISION_TAPE_MIN_SEPARATION_IN = 8
"""Distance between the two pieces of vision tape at their closest point (inches)"""

VISION_TAPE_MIN_SEPARATION_FT = VISION_TAPE_MIN_SEPARATION_IN / 12
"""Distance between the two pieces of vision tape at their closest point (feet)"""

VISION_TAPE_TOP_SEPARATION_IN = 2 * VISION_TAPE_WIDTH_IN * math.sin(VISION_TAPE_ANGLE_FROM_HORIZONTAL_RAD) + \
                                VISION_TAPE_MIN_SEPARATION_IN
"""Distance between the top point on the left rectangle and the top point on the right rectangle (inches)"""

VISION_TAPE_TOP_SEPARATION_FT = VISION_TAPE_TOP_SEPARATION_IN / 12
"""Distance between the top point on the left rectangle and the top point on the right rectangle (feet)"""

VISION_TAPE_BOTTOM_SEPARATION_IN = 2 * VISION_TAPE_LENGTH_IN * math.sin(VISION_TAPE_ANGLE_FROM_VERT_RAD) + \
                                   VISION_TAPE_MIN_SEPARATION_IN
"""Distance between the bottom point on the left rectangle and the bottom point on the right rectangle (inches)"""

VISION_TAPE_BOTTOM_SEPARATION_FT = VISION_TAPE_BOTTOM_SEPARATION_IN / 12
"""Distance between the bottom point on the left rectangle and the bottom point on the right rectangle (feet)"""

VISION_TAPE_ROTATED_HEIGHT_FT = np.matmul(_rot_mat(-VISION_TAPE_ANGLE_FROM_VERT_RAD),
                                          np.array([VISION_TAPE_WIDTH_FT, -VISION_TAPE_LENGTH_FT]))[1]

VISION_TAPE_ROTATED_WIDTH_FT = np.matmul(_rot_mat(-VISION_TAPE_ANGLE_FROM_VERT_RAD),
                                         np.array([VISION_TAPE_WIDTH_FT, VISION_TAPE_LENGTH_FT]))[0]

CENTER_LOC_FT = np.array([VISION_TAPE_TOP_SEPARATION_FT / 2, VISION_TAPE_ROTATED_HEIGHT_FT / 2])

# Vision tape coordinates
TOP_LEFT_LOCATION_FT = np.array([0, 0]) - CENTER_LOC_FT
"""The location of the top point on the left rectangle in feet. Used in cv2.solvePnP"""

BOTTOM_LEFT_LOCATION_FT = np.matmul(_rot_mat(-VISION_TAPE_ANGLE_FROM_VERT_RAD),
                                    np.array([VISION_TAPE_WIDTH_FT, -VISION_TAPE_LENGTH_FT])) - CENTER_LOC_FT
"""The location of the bottom point on the left rectangle in feet. Used in cv2.solvePnP"""

TOP_RIGHT_LOCATION_FT = np.array([VISION_TAPE_TOP_SEPARATION_FT, 0]) + TOP_LEFT_LOCATION_FT
"""The location of the top point on the right rectangle in feet. Used in cv2.solvePnP"""

BOTTOM_RIGHT_LOCATION_FT = BOTTOM_LEFT_LOCATION_FT + np.array([VISION_TAPE_BOTTOM_SEPARATION_FT, 0])
"""The location of the bottom point on the right rectangle in feet. Used in cv2.solvePnP"""

CENTER_LOC_FT = np.array([0, 0])

_two_to_three = np.array([
    [1, 0],
    [0, 1],
    [0, 0]
])

VISION_TAPE_OBJECT_POINTS = np.array([
    np.matmul(_two_to_three, TOP_LEFT_LOCATION_FT),
    np.matmul(_two_to_three, TOP_RIGHT_LOCATION_FT),
    np.matmul(_two_to_three, BOTTOM_LEFT_LOCATION_FT),
    np.matmul(_two_to_three, BOTTOM_RIGHT_LOCATION_FT)
])

PORT = int(os.getenv("V19_PORT") or 5800)
"""The port to send data over"""

CALIBRATION_FILE_LOCATION = os.getenv("V19_CALIBRATION_FILE_LOCATION") or "prod_camera_calib.pickle"
"""The path to the pickle containing the calibration information"""
