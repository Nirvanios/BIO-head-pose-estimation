import cv2
import numpy as np
from scipy.spatial.transform import Rotation


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def draw_and_show_landmarks_and_head_pose(landmarks, image, yaw='unknown', pitch='unknown', roll='unknown', info_text=''):
    """
    Draws angle and landmarks info into image and shows it
    :param landmarks: Points of interest in face
    :param image: image to draw into
    :param yaw: yaw angle in degrees
    :param pitch: pitch angle in degrees
    :param roll: roll angle in degrees
    :param info_text: info text to show
    :return: None
    """
    for pos in landmarks:
        cv2.circle(image, (int(pos[0]), int(pos[1])), 5, (0, 0, 255), -1)
    cv2.putText(image, 'Yaw: {}'.format(yaw), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(image, 'Pitch: {}'.format(pitch), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(image, 'Roll: {}'.format(roll), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(image, info_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    if not isinstance(yaw, str) and not isinstance(pitch, str) and not isinstance(roll, str):
        # Create rotation matrix
        rotation = Rotation.from_euler('yxz', [-yaw, pitch, roll], degrees=True)
        rotation_matrix = rotation.as_dcm()
        # offsets to axis end-points
        axis_points = np.float32([[50, 0, 0],
                                  [0, -50, 0],
                                  [0, 0, 50],
                                  ])

        # position in image
        position = np.array([60, image.shape[0] - 60, 0])

        axis = np.zeros((3, 3), dtype=float)
        axis[0] = np.dot(rotation_matrix, axis_points[0]) + position
        axis[1] = np.dot(rotation_matrix, axis_points[1]) + position
        axis[2] = np.dot(rotation_matrix, axis_points[2]) + position

        cv2.rectangle(image,
                      (0, image.shape[0] - 120),
                      (120, image.shape[0]),
                      (255, 255, 255),
                      -1)
        cv2.line(image, (int(position[0]), int(position[1])), (int(axis[1][0]), int(axis[1][1])), (0, 255, 0), 3)
        cv2.line(image, (int(position[0]), int(position[1])), (int(axis[0][0]), int(axis[0][1])), (255, 0, 0), 3)
        cv2.line(image, (int(position[0]), int(position[1])), (int(axis[2][0]), int(axis[2][1])), (0, 0, 255), 3)

    cv2.imshow('Out', image)
