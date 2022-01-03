import os

import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.models import load_model


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


def define_cnn_model(width, height):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(width, height, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(16, activation='softmax'))

    # Stochastic gradient descent optimisation
    opt = SGD(learning_rate=0.01, momentum=0.9)

    # model.summary()
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


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


def train(width, height, X_train, y_train, model_path):
    model = define_cnn_model(width, height)
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)
    model.save(model_path)


def test(X_test, y_test, model_path):
    model = load_model(model_path)
    _, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f'Accuracy: > %.3f' % (acc * 100.0) + '%')


def classify(verbose=0, extracted_characters_dir=''):
    model = load_model('final_model.h5')

    chars, file_names = [], []
    for subdir, dirs, files in os.walk(extracted_characters_dir):
        for file in sorted(files):
            photo = Image.open(os.path.join(subdir, file)).convert('L')  # Greyscale
            X_pred_i = normalise_data(np.asarray(photo))

            chars.append(X_pred_i)
            file_names.append(os.path.join(subdir, file))

    X_pred = np.asarray(chars).reshape((len(chars), 45, 45, 1))
    y_pred = model.predict(X_pred, verbose=0)

    predicted_labels = []
    print()
    for idx, y_pred_i in enumerate(y_pred):
        predicted_labels.append(np.argmax(y_pred_i))

        if verbose:
            print(f'Character: {file_names[idx]}')
            print(f'Predicted value: {get_character(np.argmax(y_pred_i))}, with accuracy of %.3f' % (
                    max(y_pred_i) * 100.0) + '%')
            if max(y_pred_i) <= 0.5:
                print('WARNING: Accuracy is below 50%, classification might be incorrect.')
            print()

    math_expression = ' '.join([get_character(label) for label in predicted_labels])
    return math_expression
