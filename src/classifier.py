import os

import numpy as np
from PIL import Image
from tensorflow.python.keras.models import load_model

from scripts.util import normalise_data


def get_character(label):
    if label == 10:
        return '+'
    elif label == 11:
        return '-'
    elif label == 12:
        return '*'
    elif label == 13:
        return '/'
    elif label == 14:
        return '('
    elif label == 15:
        return ')'
    else:
        return str(label)


def print_prediction_information(file_name, y_pred_i):
    print(f'Character: {file_name}')
    print(f'Predicted value: {get_character(np.argmax(y_pred_i))}, with accuracy of %.3f' % (
            max(y_pred_i) * 100.0) + '%')
    if max(y_pred_i) <= 0.5:
        print('WARNING: Accuracy is below 50%, classification might be incorrect.')
    print()


def classify(model_path, extracted_characters_dir, width, height, verbose):
    model = load_model(model_path)

    file_names, chars = [], []

    for subdir, dirs, files in os.walk(extracted_characters_dir):
        for file in sorted(files):
            file_names.append(os.path.join(subdir, file))

            photo = Image.open(os.path.join(subdir, file)).convert('L')  # Greyscale
            X_pred_i = normalise_data(np.asarray(photo))
            chars.append(X_pred_i)

    X_pred = np.asarray(chars).reshape((len(chars), width, height, 1))
    y_pred = model.predict(X_pred, verbose=0)

    predicted_labels = []
    print()

    for idx, y_pred_i in enumerate(y_pred):
        predicted_labels.append(np.argmax(y_pred_i))

        if verbose:
            print_prediction_information(file_names[idx], y_pred_i)

    math_expression = ' '.join([get_character(label) for label in predicted_labels])
    return math_expression
