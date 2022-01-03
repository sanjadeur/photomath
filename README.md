# Photomath
Photomath is a deep learning based tool which enables one to pass a photo of a math expression and get the result.


## Requirements
* Git
* Python 3.x (x >= 7)
* Pip >= 19.0


## Installation
1. Clone the repository
   ```shell
   git clone ... photomath && cd photomath
   ```

2. Create virtual environment
   * Using venv
      ```shell
      python3.x -m venv photomath_venv
      source photomath_venv/bin/activate
      ```

    * or conda
      ```shell
      conda create --name photomath python=3.x
      conda activate photomath
      ```

3. Install requirements
   ```shell
   pip install -r requirements.txt
   ```

4. Install appropriate TensorFlow version

   https://www.tensorflow.org/install
   ```shell
   pip install --upgrade tensorflow
   ```
   

## Usage
### Photomath
   ```shell
    python src/photomath.py -p <photo_path> [options ...]

      options:
        -p, --photo_path <str>
          required
          path to the photo of a math expression  
        --width <int>
          default: 45
          width of the photos in the dataset
        --height <int>
          default: 45
          height of the photos in the dataset
        --dest <str>
          default: 'resources/extracted_characters'
          path to the directory where extracted characters will be stored
        --model_path <str>
          default: 'final_model.h5'
          path of the trained model
        --verbose <int>
          default: 1
          choose 1 for displaying the prediction information, 0 otherwise

    NOTE: Please run scripts/train.py first in case there is no saved model.
   ```

### Train
   ```shell
    python scripts/train.py [options ...]

      options:
        --dataset_path <str>
          default: resources/homogenised_dataset
          path to the homogenised characters dataset
        --width <int>
          default: 45
          width of the photos in the dataset
        --height <int>
          default: 45
          height of the photos in the dataset
        --model_path <str>
          default: 'final_model.h5'
          path for storing the trained model in H5 file

    NOTE: Please run scripts/homogenise_data.py first in case dataset is not homogeneous.
   ```

### Test
   ```shell
    python scripts/test.py [options ...]

      options:
        --dataset_path <str>
          default: resources/homogenised_dataset
          path to the homogenised characters dataset
        --width <int>
          default: 45
          width of the photos in the dataset
        --height <int>
          default: 45
          height of the photos in the dataset
        --model_path <str>
          default: 'final_model.h5'
          path of the trained model

    NOTE: Please run scripts/homogenise_data.py first in case dataset is not homogeneous.
          Please run scripts/train.py first in case there is no saved model.
   ```

### Homogenise data
   ```shell
    python scripts/test.py [options ...]

      options:
        --dataset_path <str>
          default: resources/homogenised_dataset
          path to the homogenised characters dataset
        --no_of_files <int>
          default: 3000
          number of examples for each character
        --dest <str>
          default: resources/homogenised_dataset
          path to the directory for storing the homogenised characters dataset
   ```