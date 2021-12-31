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

        # Create a bounding box
        cv2.rectangle(photo, (left - 5, top - 5), (left + width + 5, top + height + 5), (0, 255, 0), 3)

        # Avoid noise (e.g. dot in wrong_expression.jpg example)
        if width > 35 and height > 10 or width > 10 and height > 35:
            characters.append(threshold[top - 5:top + height + 5, left - 5:left + width + 5])

    return characters


def save_characters(photo_name, characters):
    for idx, character in enumerate(characters, start=1):
        cv2.imwrite(f'../chars/{photo_name}_{idx}.jpg', character)


if __name__ == '__main__':
    photo_name = 'simple_expression'
    photo_path = f'../data/{photo_name}.jpg'

    characters = extract_characters(photo_path)
    save_characters(photo_name, characters)
