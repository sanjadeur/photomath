import os
import sys
from argparse import ArgumentParser

from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD

from util import load_dataset, normalise_data


def parse_arguments():
    parser = ArgumentParser(description='Photomath - train the model',
                            epilog='NOTE: Please run scripts/homogenise_data.py first in case dataset is not homogenous.')

    parser.add_argument('--dataset_path', type=str, default='resources/homogenised_dataset',
                        help='path to the homogenised characters dataset')

    parser.add_argument('--width', type=int, default=45,
                        help='width of the photos in the dataset')

    parser.add_argument('--height', type=int, default=45,
                        help='height of the photos in the dataset')

    parser.add_argument('--model_path', type=str, default='final_model.h5',
                        help='path for storing the trained model in H5 file')

    return parser.parse_args()


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


def train():
    # Load dataset
    X_train, y_train, X_test, y_test = load_dataset(args.dataset_path, args.width, args.height)

    # Normalise data - scale pixels
    X_train, X_test = normalise_data(X_train), normalise_data(X_test)

    # Train the model
    model = define_cnn_model(args.width, args.height)
    model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=0)

    # Save the model
    model.save(args.model_path)


if __name__ == '__main__':
    args = parse_arguments()

    if not os.path.isdir(args.dataset_path):
        sys.stderr.write('ERROR: Path to the homogenised characters dataset does not exist.\n')
        exit(0)

    train()
