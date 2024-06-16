SIZE = (512, 512)
HEIGHT = 512
WIDTH = 512

SATURATION_MIN=60 # max 100
BRIGHTNESS_MIN=60 # max 100

from PIL import Image
import os
import colorsys


def is_happy_color(s, v, brightness_min, saturation_min):

    s = int(s * 100)   # Convert to percentage 
    v = int(v * 100)  

    is_bright = v >= brightness_min
    is_saturated = s >= saturation_min

    return is_bright and is_saturated


def adjust_color(h, s, v, brightness_min, saturation_min):

    brightness_min /= 100.0 # Convert from percentage
    saturation_min /= 100.0

    s = max(s, saturation_min)
    v = max(v, brightness_min)
    
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r, g, b = int(r * 255), int(g * 255), int(b * 255) 
    
    return (r, g, b)


def  is_in_circle(x, y):
    circle_center_x, circle_center_y = (WIDTH/2), (HEIGHT/2)
    radius = (HEIGHT/2)
    sq_distance = ((x - circle_center_x) ** 2 + (y - circle_center_y) ** 2) # с**2 = a**2 + b**2
    return sq_distance <= radius ** 2


def verify_badge(image_path, brightness_min, saturation_min):

    try:
        img = Image.open(image_path).convert("RGBA")
    except FileNotFoundError:
        return False, f"File not found: {image_path}"
    except Exception as e:
        return False, f"Error opening image: {str(e)}"
    
    if img.size != SIZE:
        return False, "Invalid size"

    pixels_len = 0
    bad_colors_len = 0

    if brightness_min is None:
        brightness_min = BRIGHTNESS_MIN
    if saturation_min is None:
        saturation_min = SATURATION_MIN

    for x in range(WIDTH):
        for y in range(HEIGHT):
            pixel = img.getpixel((x, y))
            if len(pixel) == 4 and pixel[3] != 0:
                if not is_in_circle(x, y):
                    return False, "Non-transparent pixels found"
                pixels_len += 1

                r, g, b = pixel[:3]  
                _, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)  # convert to HSV 

                if not is_happy_color(s, v, brightness_min, saturation_min):
                    bad_colors_len +=1

    happy_colors = (1 - (bad_colors_len/pixels_len))
    if happy_colors < 0.9:
        return False, "Colors do not convey a happy feeling"
    
    return True, "Badge is valid"



def convert_image(image_path, brightness_min, saturation_min):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        return False, f"File not found: {image_path}"
    except Exception as e:
        return False, f"Error opening image: {str(e)}"
    
    base_name = os.path.basename(image_path)
    
    image_name, extension = os.path.splitext(base_name)
    save_path = f"./processed/{image_name}.png"

    if extension != '.png':
        try:
            img.save(save_path)
        except OSError:
            return False, f"Cannot convert. Unsupported file type."
        
    img = img.resize(SIZE).convert("RGBA")

    if brightness_min is None:
        brightness_min = BRIGHTNESS_MIN
    if saturation_min is None:
        saturation_min = SATURATION_MIN

    for x in range(WIDTH):
        for y in range(HEIGHT):
            pixel = img.getpixel((x, y))
            if len(pixel) == 4 and pixel[3] != 0:
                if not is_in_circle(x, y):
                    pixel = (pixel[0], pixel[1], pixel[2], 0)
                else:

                    r, g, b = pixel[:3]
                    h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0) # convert to HSV 

                    if not is_happy_color(s, v, brightness_min, saturation_min):
                        r, g, b = adjust_color(h, s, v, brightness_min, saturation_min)
                        pixel = (r, g, b, pixel[3]) 
                img.putpixel((x, y), pixel)

    img.save(save_path)
    return True, "Image converted, you can find it here: " + save_path
