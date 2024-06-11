import unittest
from main import verify_badge, convert_image
from parameterized import parameterized
import os

class TestImageFunc(unittest.TestCase):
    
	# SATURATION_MIN = 60 # max 100
	# BRIGHTNESS_MIN = 60 # max 100
    @parameterized.expand([
        ("invalid_size", "./test_images/friends.png", (False, "Invalid size")),
        ("invalid_ntp_1", "./test_images/facebook.png", (False, "Non-transparent pixels found")),
        ("invalit_ntp_2", "./test_images/orange.png", (False, "Non-transparent pixels found")),
        ("invalid_colors_1", "./test_images/alien.png", (False, "Colors do not convey a happy feeling")), 
       	("invalid_colors_2", "./test_images/insta.png", (False, "Colors do not convey a happy feeling")),
        ("valid_badge_1", "./test_images/ball.png", (True, "Badge is valid")),
        ("valid_badge_2", "./test_images/google.png", (True, "Badge is valid")),
        
    ])
    
    def test_verify_badge(self, name, input_path, expected_output):
        with self.subTest(name=name):
            result = verify_badge(input_path)
            self.assertEqual(result, expected_output)

    @parameterized.expand([
        ("valid_png_one_color", "./test_images/orange.png", (True, "Badge is valid")),
        ("valid_png_1", "./test_images/alien.png", (True, "Badge is valid")),
        ("valid_png_2", "./test_images/bird.png", (True, "Badge is valid")),
        ("valid_png_4", "./test_images/yellow.png", (True, "Badge is valid")),
        ("valid_webp", "./test_images/yellow_bright.webp", (True, "Badge is valid")),
        ("valid_jpg", "./test_images/chicken.jpg", (True, "Badge is valid")),
        ("valid_bmp","test_images/tiger.bmp",  (True, "Badge is valid")),
    ])
    
    def test_convert_image_result(self, name, input_path, expected_output):
        with self.subTest(name=name):
            filename, _ = os.path.splitext(os.path.basename(input_path))
            convert_image(input_path)
            pr_img_path = os.path.join("./processed", filename + ".png")
            result = verify_badge(pr_img_path)
            self.assertEqual(result, expected_output)

        
if __name__ == '__main__':
    unittest.main()