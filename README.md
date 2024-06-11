# test_assignment

## Task: 
We want users to upload a badge: an avatar within a circle. Create a function taking a PNG as input and verifying that:
 - Size = 512x512
 - The only non-transparent pixels are within a circle
 - The colors in the badge give a "happy" feeling

Additionally, you can create a parallel function that converts the given image (of any format) into the specified object.

## Implementation: 

The task is written in Python, utilizing OpenCV and Pillow libraries for image processing. K-means clustering method was used to select main colors from pictures. 

## Usage:
To use functions, run the script provided below. In addition, you can provide two env variables (*BRIGHTNESS_MIN*, *SATURATION_MIN*) to configure the converting and validation of 'happy colors', in order to do that, create an **.env** file and put them there. However, it is not necessary and the default values will be used in case nothing is provided.

```bash
python3 -m venv badge_env
source badge_env/bin/activate
pip install -r requirements.txt
mkdir processed
python3 main.py <path_to_image>
```
## Testing:  
There are unit tests in the repository, which can be run using the script, provided below
```bash
python3 -m venv badge_env
source badge_env/bin/activate
pip install -r requirements.txt
mkdir processed
python3 verify_convert_test.py
```
