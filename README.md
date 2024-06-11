# test_assignment

## Task: 
We want users to upload a badge: an avatar within a circle. Create a function taking a PNG as input and verifying that:
 - Size = 512x512
 - The only non-transparent pixels are within a circle
 - The colors in the badge give a "happy" feeling

Additionally, you can create a parallel function that converts the given image (of any format) into the specified object.

## Implementation: 

The task is written in Python, utilizing OpenCV and Pillow libraries for image processing. K-means clustering method was used to select main colors from pictures. 

## To test functions: 

```bash
python3 -m venv badge_env
source badge_env/bin/activate
pip install -r requirements.txt
python3 badge_test.py
```
