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

VIS_WID_CARTESIAN_FT = VISION_TAPE_WIDTH_IN * math.sin(VISION_TAPE_ANGLE_FROM_HORIZONTAL_RAD) / 12
VIS_HEI_CARTESIAN_FT = VISION_TAPE_LENGTH_IN * math.sin(VISION_TAPE_ANGLE_FROM_VERT_RAD) / 12

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

TOTAL_HEIGHT_IN = math.sin(VISION_TAPE_ANGLE_FROM_VERT_RAD) * VISION_TAPE_WIDTH_IN + \
                  math.sin(VISION_TAPE_ANGLE_FROM_HORIZONTAL_RAD) * VISION_TAPE_LENGTH_IN

BT_LEFT_2_IN = np.array((VISION_TAPE_LENGTH_IN * math.sin(VISION_TAPE_ANGLE_FROM_VERT_RAD) + VISION_TAPE_MIN_SEPARATION_IN/2,
              -TOTAL_HEIGHT_IN/2), dtype=np.double)
BT_RIGHT_2_IN = BT_LEFT_2_IN + np.array((math.cos(VISION_TAPE_ANGLE_FROM_VERT_RAD) * VISION_TAPE_WIDTH_IN,
                                math.sin(VISION_TAPE_ANGLE_FROM_VERT_RAD) * VISION_TAPE_WIDTH_IN), dtype=np.double)
TP_LEFT_2_IN = np.array((VISION_TAPE_MIN_SEPARATION_IN/2,
                 TOTAL_HEIGHT_IN/2 - math.sin(VISION_TAPE_ANGLE_FROM_VERT_RAD) * VISION_TAPE_WIDTH_IN), dtype=np.double)
TP_RIGHT_2_IN = np.array((VISION_TAPE_MIN_SEPARATION_IN/2 + math.cos(VISION_TAPE_ANGLE_FROM_VERT_RAD) * VISION_TAPE_WIDTH_IN,
                 TOTAL_HEIGHT_IN/2), dtype=np.double)

BT_RIGHT_1_IN = np.array((BT_LEFT_2_IN[0] * -1, BT_LEFT_2_IN[1]), dtype=np.double)
BT_LEFT_1_IN = np.array((BT_RIGHT_2_IN[0] * -1, BT_RIGHT_2_IN[1]), dtype=np.double)
TP_RIGHT_1_IN = np.array((TP_LEFT_2_IN[0] * -1, TP_LEFT_2_IN[1]), dtype=np.double)
TP_LEFT_1_IN = np.array((TP_RIGHT_2_IN[0] * -1, TP_RIGHT_2_IN[1]), dtype=np.double)



_two_to_three = np.array([
    [1, 0],
    [0, 1],
    [0, 0]
])

VISION_TAPE_OBJECT_POINTS = np.array([
    np.matmul(_two_to_three, BT_LEFT_1_IN/12),
    np.matmul(_two_to_three, TP_LEFT_1_IN/12),
    np.matmul(_two_to_three, BT_RIGHT_2_IN/12),
    np.matmul(_two_to_three, TP_RIGHT_2_IN/12)
])

print(VISION_TAPE_OBJECT_POINTS)

PORT = int(os.getenv("V19_PORT") or 5800)
"""The port to send data over"""

CALIBRATION_FILE_LOCATION = "prod_camera_calib.pickle"
"""The path to the pickle containing the calibration information"""
