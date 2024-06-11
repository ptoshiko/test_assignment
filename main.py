import sys
from verify_convert import *
from dotenv import load_dotenv


def get_brightness_min():
    brightness_min = os.getenv("BRIGHTNESS_MIN")
    if brightness_min is None:
        return None
    
    try:
        converted_brightness_min = float(os.getenv("BRIGHTNESS_MIN")) # Convert the string to a float
    except ValueError:
        print("Warning: BRIGHTNESS_MIN must be a number, keeping it None")
        return None
    return converted_brightness_min

def get_saturation_min():
    saturation_min = os.getenv("SATURATION_MIN")
    if saturation_min is None:
        return None
    
    try:
        converted_saturation_min = float(saturation_min)  # Convert the string to a float
    except ValueError:
        print("Warning: SATURATION_MIN must be a number, keeping it None")
        return None
    return converted_saturation_min


def main():
    if len(sys.argv) != 2:
        print("Invalid arguments")
        return
    saturation_min = None
    brightness_min = None
    if os.path.isfile('.env'):
        load_dotenv()
        brightness_min = get_brightness_min()
        saturation_min = get_saturation_min()
    
    image_path = sys.argv[1]
    print("Verifying image...")
    is_valid, message = verify_badge(image_path, brightness_min, saturation_min)
    print(message)

    if not is_valid:
        print("Converting to valid format...")
        _, message = convert_image(image_path, brightness_min, saturation_min)
        print(message)

if __name__ == "__main__":
    main()