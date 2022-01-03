import os
import sys
from argparse import ArgumentParser

from tensorflow.python.keras.models import load_model

from util import load_dataset, normalise_data


def parse_arguments():
    parser = ArgumentParser(description='Photomath - test the model',
                            epilog='NOTE: Please run scripts/homogenise_data.py first in case dataset is not homogenous.\n'
                                   'Please run scripts/train.py first in case there is no saved model.')

    parser.add_argument('--dataset_path', type=str, default='resources/homogenised_dataset',
                        help='path to the homogenised characters dataset')

    parser.add_argument('--width', type=int, default=45,
                        help='width of the photos in the dataset')

    parser.add_argument('--height', type=int, default=45,
                        help='height of the photos in the dataset')

    parser.add_argument('--model_path', type=str, default='final_model.h5',
                        help='path of the trained model')

    return parser.parse_args()


def test():
    if not os.path.isdir(args.dataset_path):
        sys.stderr.write('ERROR: Path to the homogenised characters dataset does not exist.\n')
        exit(0)

    # Load dataset
    X_train, y_train, X_test, y_test = load_dataset(args.dataset_path, args.width, args.height)

    # Normalise data - scale pixels
    X_train, X_test = normalise_data(X_train), normalise_data(X_test)

    # Load the model
    model = load_model(args.model_path)

    # Test the model
    _, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f'Accuracy: > %.3f' % (acc * 100.0) + '%')


if __name__ == '__main__':
    args = parse_arguments()

    if not os.path.isdir(args.dataset_path):
        sys.stderr.write('ERROR: Path to the homogenised characters dataset does not exist.\n')
        exit(0)

    if not os.path.exists(args.model_path):
        sys.stderr.write('ERROR: Path for storing the trained model does not exist.\n')
        exit(0)

    test()
