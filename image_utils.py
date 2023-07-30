
import cv2
from datetime import datetime
import re
from collections import defaultdict
import os
import logging


def setup_logging():
    # Configure the logging format
    logging.basicConfig(format='%(asctime)s - %(levelname)s  - Thread %(thread)d - %(message)s', level=logging.INFO)
    # Create a logger
    logger = logging.getLogger(__name__)
    return logger

def get_image_files(folder_path):
    return [filename for filename in os.listdir(folder_path) if filename.endswith('.png')]

def get_camera_id(filename):
    return filename[:3]

def get_timestamp(filename):
    timestamp_regex1 = r"\d{13}"  # Matches 13 digits in a row (e.g., c20-1616776357476)
    timestamp_regex2 = r"\d{4}_\d{2}_\d{2}__\d{2}_\d{2}_\d{2}"  # Matches the second format (e.g., c21_2021_03_26__14_32_43)

    # Try matching the first timestamp format
    match1 = re.search(timestamp_regex1, filename)
    if match1:
        return int(match1.group())

    # If the first format doesn't match, try the second format
    match2 = re.search(timestamp_regex2, filename)
    if match2:
        dt_str = match2.group().replace("_", ":")
        dt_obj = datetime.strptime(dt_str, "%Y:%m:%d::%H:%M:%S")
        return int(dt_obj.timestamp() * 1000)

    return None  # If no match is found, return None

def parse_timestamp(timestamp_str):
    try:
        return int(timestamp_str)
    except ValueError:
        try:
            dt_obj = datetime.strptime(timestamp_str, "%Y_%m_%d__%H_%M_%S")
            return int(dt_obj.timestamp() * 1000)
        except ValueError:
            return None

def resize_image(image, desired_width, desired_height):
    if image is None or image.size == 0:  # Check if the image is empty
        return None

    # Check if the image already has the desired resolution
    current_height, current_width, _ = image.shape
    if current_width == desired_width and current_height == desired_height:
        return image

    # Resize the image to the desired resolution
    return cv2.resize(image, (desired_width, desired_height))

def get_camera_resolution(camera_id):
    # For all cameras except c10, use 1920x1080
    if camera_id != "c10":
        return 1920, 1080
    else:
        return 640,480
    
def group_images_by_camera_id(folder_path):
    image_filenames = [filename for filename in os.listdir(folder_path) if filename.endswith('.png')]
    image_paths = [os.path.join(folder_path, filename) for filename in image_filenames]

    # Group images by camera ID
    camera_images = defaultdict(list)
    for image_path in image_paths:
        camera_id = get_camera_id(os.path.basename(image_path))
        camera_images[camera_id].append(image_path)

    return camera_images
