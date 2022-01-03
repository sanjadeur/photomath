import os

import cv2
import numpy as np


def extract_contours(photo):
    gaussian_blur = cv2.GaussianBlur(photo, (11, 11), 0)
    retval, threshold = cv2.threshold(gaussian_blur, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, threshold


def extract_characters(photo_path):
    photo = cv2.imread(photo_path, 0)  # Greyscale
    contours, threshold = extract_contours(photo)
    contour_index_LtoR = np.argsort([cv2.boundingRect(contour)[0] for contour in contours])
    characters = []

    for idx in contour_index_LtoR:
        photo_height, photo_width = photo.shape
        left, top, width, height = cv2.boundingRect(contours[idx])

        # Avoid blank photo
        if height == photo_height and width == photo_width:
            continue

        # Avoid noise (e.g. dot in wrong_expression.jpg example)
        if width > 35 and height > 5 or width > 5 and height > 35:
            # Bounding box is 5 pixels
            characters.append(threshold[top - 5:top + height + 5, left - 5:left + width + 5])

    return characters


def save_characters(characters, photo_name, width, height, dest):
    for idx, character in enumerate(characters, start=1):
        resized_photo = cv2.resize(character, (width, height), interpolation=cv2.INTER_AREA)

        dir_name = os.path.join(dest, photo_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        cv2.imwrite(os.path.join(dir_name, f'char_{idx}.jpg'), resized_photo)


def detect(photo_path, photo_name, width, height, dest):
    characters = extract_characters(photo_path)
    if len(characters) == 0:
        return False

    save_characters(characters, photo_name, width, height, dest)
    return True
