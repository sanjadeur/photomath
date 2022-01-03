import os

import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical


def get_label(subdir):
    char = subdir.split('/')[-1]
    if char == '+':
        return 10
    elif char == '-':
        return 11
    elif char == 'x':
        return 12
    elif char == 'div':
        return 13
    elif char == '(':
        return 14
    elif char == ')':
        return 15
    else:
        return int(char)


def load_dataset(dataset_path, width, height):
    # Convert photos to numpy arrays and add labels
    X, y = [], []
    for subdir, dirs, files in os.walk(dataset_path):
        for file in files:
            photo = Image.open(os.path.join(subdir, file)).convert('L')  # Greyscale
            X.append(np.asarray(photo))
            y.append(get_label(subdir))

    # Divide dataset into training and test set, by 85% and 15% respectively
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    X_train, X_test, y_train, y_test = np.asarray(X_train), np.asarray(X_test), np.asarray(y_train), np.asarray(y_test)

    # Reshape dataset to have one channel (black and white photo)
    X_train = X_train.reshape((X_train.shape[0], width, height, 1))
    X_test = X_test.reshape((X_test.shape[0], width, height, 1))

    # Target values are one-hot encoded
    y_train, y_test = to_categorical(y_train), to_categorical(y_test)

    return X_train, y_train, X_test, y_test


def normalise_data(data):
    data_norm = data.astype('float32')
    return data_norm / 255.0  # Normalize to range 0-1
