# Photomath
Photomath is a deep learning based tool which enables one to pass a photo of a math expression and get the result.

## Requirements
* Git
* Python 3.x (x >= 7)
* Pip >= 19.0
* Appropriate CUDA version

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

4. Install appropriate TensorFlow version (built for specific CUDA version)

   https://www.tensorflow.org/install
   ```shell
   pip install --upgrade tensorflow
   ```