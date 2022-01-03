from argparse import ArgumentParser

from detector import detect

if __name__ == "__main__":
    parser = ArgumentParser(description='Photomath')

    # Detector specific args
    parser.add_argument('--photo_path', type=str, help='Path to the photo of a math expression')
    parser.add_argument('--width', type=int, default=45, help='Width of the photos in the dataset')
    parser.add_argument('--height', type=int, default=45, help='Height of the photos in the dataset')
    parser.add_argument('--dest', type=str, default='resources/extracted_characters',
                        help='Path to the directory where extracted characters will be stored')

    args = parser.parse_args()

    detect(args.photo_path, args.width, args.height, args.dest)
