import os
import sys
from argparse import ArgumentParser

from classifier import classify
from detector import detect
from solver import solve


def parse_arguments():
    parser = ArgumentParser(description='Photomath',
                            epilog='NOTE: Please run scripts/train.py first in case there is no saved model.')

    parser.add_argument('-p', '--photo_path', type=str, required=True,
                        help='path to the photo of a math expression')

    parser.add_argument('--width', type=int, default=45,
                        help='width of the photos in the dataset')

    parser.add_argument('--height', type=int, default=45,
                        help='height of the photos in the dataset')

    parser.add_argument('--dest', type=str, default='resources/extracted_characters',
                        help='path to the directory where extracted characters will be stored')

    parser.add_argument('--model_path', type=str, default='final_model.h5',
                        help='path of the trained model')

    parser.add_argument('--verbose', type=int, default=1,
                        help='choose 1 for displaying the prediction information, 0 otherwise')

    return parser.parse_args()


def detection():
    print('\nFIRST PART: Detecting single characters from the photo...')

    if not os.path.isfile(args.photo_path):
        sys.stderr.write('ERROR: Photo of a math expression does not exist.\n')
        exit(0)

    if not os.path.isdir(args.dest):
        sys.stderr.write('ERROR: Directory where extracted characters will be stored does not exist.\n')
        exit(0)

    photo_name = args.photo_path.strip().split('/')[-1].split('.')[0]
    is_detected = detect(args.photo_path, photo_name, args.width, args.height, args.dest)

    if not is_detected:
        print('There are no characters detected in the given photo.\n')
        exit(0)

    print(f'Characters are detected and extracted to "{os.path.join(args.dest, photo_name)}".')

    return photo_name


def classification(photo_name):
    print('\nSECOND PART: Classifying extracted characters...\n')

    if not os.path.exists(args.model_path):
        sys.stderr.write('ERROR: Path of the trained model does not exist.\n')
        exit(0)

    if not (args.verbose == 0 or args.verbose == 1):
        sys.stderr.write('ERROR: Verbose flag should be either 0 or 1.\n')
        exit(0)

    extracted_characters_dir = os.path.join(args.dest, photo_name)
    math_expression = classify(args.model_path, extracted_characters_dir, args.width, args.height, args.verbose)

    print(f'Recognised math expression: "{math_expression}"')

    return math_expression


def solution(math_expression):
    print('\nTHIRD PART: Solving the math expression...')

    try:
        result = solve(math_expression)

        if result is None:
            sys.stderr.write('ERROR: Math expression does not follow the infix notation.\n')
            exit(0)

        print('Final result: %.3f' % result)

    except ZeroDivisionError:
        sys.stderr.write('ERROR: Division by zero is not allowed.\n')
        exit(0)


if __name__ == "__main__":
    args = parse_arguments()

    # First part: detection
    photo_name = detection()

    # Second part: classification
    math_expression = classification(photo_name)

    # Third part: solution
    solution(math_expression)
