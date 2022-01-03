import os
import random
import shutil
from argparse import ArgumentParser

random.seed(42)


def parse_arguments():
    parser = ArgumentParser(description='Photomath - homogenise the data')

    parser.add_argument('--dataset_path', type=str, default='resources/dataset',
                        help='Path to the characters dataset')

    parser.add_argument('--no_of_files', type=int, default=3000,
                        help='Number of examples for each character')

    parser.add_argument('--dest', type=str, default='resources/homogenised_dataset',
                        help='Path for storing the homogenised characters dataset')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    for subdir, dirs, files in os.walk(args.dataset_path):
        subdir_name = subdir.split('/')[-1]
        if subdir_name == args.dataset_path.split('/')[-1]:
            continue

        dest = os.path.join(args.dest, subdir_name)
        if not os.path.exists(dest):
            os.makedirs(dest)

        # Remove examples
        if len(files) >= args.no_of_files:
            files_to_copy = random.sample(files, args.no_of_files)
            for file in files_to_copy:
                shutil.copy(os.path.join(subdir, file), dest)

        # Repeat examples
        else:
            residue = args.no_of_files % len(files)
            files_to_copy = random.sample(files, residue)
            for file in files_to_copy:
                shutil.copy(os.path.join(subdir, file), dest)

            number_of_repetitions = args.no_of_files // len(files)
            for i in range(number_of_repetitions):
                for file in files:
                    file_name, file_extension = file.split('.')
                    final_file = f'{file_name}_{i}.{file_extension}'
                    shutil.copy(os.path.join(subdir, file), os.path.join(dest, final_file))
