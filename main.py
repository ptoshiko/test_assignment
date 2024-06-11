SIZE = (512, 512)
KSIZE = (5, 5)

SCALE_FACTOR = 4
MASK_PATH = "./mask.png"

SATURATION_MIN = 60 # max 100
BRIGHTNESS_MIN = 60 # max 100


N_CLUSTERS = 7

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import cv2
import os


def create_mask():
    mask = Image.new('L', (512, 512), 0)
    np_mask = np.array(mask)
    center = (SIZE[0] // 2, SIZE[1] // 2)
    radius = SIZE[0] // 2
    cv2.circle(np_mask, center, radius, 255, thickness=-1)
    
    pil_mask = Image.fromarray(np_mask)
    pil_mask.save(MASK_PATH)
    return np_mask


def is_happy_color(color):

    color_hsv = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
    _, s, v = color_hsv
    
    is_bright = v > BRIGHTNESS_MIN
    is_saturated = s > SATURATION_MIN
    
    return is_bright and is_saturated


def check_colors(np_img):
    
    non_transparent = np_img[:, :, 3] != 0
    colors = np_img[non_transparent, :3].reshape(-1, 3)
    
    unique_colors = np.unique(colors, axis=0)
    
    n_clusters = min(N_CLUSTERS, len(unique_colors))
    
    if len(unique_colors) < N_CLUSTERS:
        happy_colors = sum(1 for color in unique_colors if is_happy_color(color)) / len(unique_colors)

    else:
        kmeans = KMeans(n_clusters=n_clusters).fit(colors)
        happy_colors = sum(1 for center in kmeans.cluster_centers_ if is_happy_color(center)) / N_CLUSTERS
    if happy_colors < 0.6:
        return False
    return True


def adjust_colors(np_img):
    
	alpha_channel = np_img[:, :, 3]
	non_transparent_mask = np_img[:, :, 3] != 0
	hsv_img = cv2.cvtColor(np_img[:, :, :3], cv2.COLOR_RGB2HSV)

	h, s, v = cv2.split(hsv_img)
    
	s[non_transparent_mask] = np.maximum(s[non_transparent_mask], SATURATION_MIN)
	v[non_transparent_mask] = np.maximum(v[non_transparent_mask], BRIGHTNESS_MIN)
    
	adjusted_hsv_img = cv2.merge([h, s, v])
    
	adjusted_rgb_img = cv2.cvtColor(adjusted_hsv_img, cv2.COLOR_HSV2RGB)
    
	adjusted_rgba_img = np.dstack((adjusted_rgb_img, alpha_channel))
    
	return adjusted_rgba_img



def verify_badge(image_path):

    try:
        img = Image.open(image_path).convert("RGBA")
    except FileNotFoundError:
        return False, f"File not found: {image_path}"
    except Exception as e:
        return False, f"Error opening image: {str(e)}"
    
    if img.size != SIZE:
        return False, "Invalid size"

    np_img = np.array(img)
    non_transparent = np_img[:, :, 3] != 0
    
    np_mask = create_mask()
    
    # boolean array where True indicates pixels outside the circle
    outside_circle = non_transparent & (np_mask == 0)
    if (np.any(outside_circle)):
          return False, "Non-transparent pixels found"
    
    if not (check_colors(np_img)):
        return False, "Colors do not convey a happy feeling"
    
    return True, "Badge is valid"



def convert_image(image_path):
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        return False, f"File not found: {image_path}"
    except Exception as e:
        return False, f"Error opening image: {str(e)}"
    
    base_name = os.path.basename(image_path)
    
    image_name, extension = os.path.splitext(base_name)
    save_path = f"./processed/{image_name}.png"

    if extension != '.png':
        try:
            image.save(save_path)
        except OSError:
            return False, f"Cannot convert. Unsupported file type."
        
    image = image.resize((512, 512)).convert("RGBA")

    np_mask = create_mask()
    np_img = np.array(image)
    
    np_img[np_mask == 0] = [0, 0, 0, 0]  # set outside pixels to transparent
    if not (check_colors(np_img)):
        adjusted_np_img = adjust_colors(np_img)
        img = Image.fromarray(adjusted_np_img)
    else:
        img = Image.fromarray(np_img)
    img.save(save_path)
        
    return True, "Image converted"





