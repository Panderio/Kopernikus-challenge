import os
import cv2
import imutils
import os
import re
from datetime import datetime

def draw_color_mask(img, borders, color=(0, 0, 0)):
    h = img.shape[0]
    w = img.shape[1]

    x_min = int(borders[0] * w / 100)
    x_max = w - int(borders[2] * w / 100)
    y_min = int(borders[1] * h / 100)
    y_max = h - int(borders[3] * h / 100)

    img = cv2.rectangle(img, (0, 0), (x_min, h), color, -1)
    img = cv2.rectangle(img, (0, 0), (w, y_min), color, -1)
    img = cv2.rectangle(img, (x_max, 0), (w, h), color, -1)
    img = cv2.rectangle(img, (0, y_max), (w, h), color, -1)

    return img


def preprocess_image_change_detection(img, gaussian_blur_radius_list=None, black_mask=(5, 10, 5, 0)):
    gray = img.copy()
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    if gaussian_blur_radius_list is not None:
        for radius in gaussian_blur_radius_list:
            gray = cv2.GaussianBlur(gray, (radius, radius), 0)

    gray = draw_color_mask(gray, black_mask)

    return gray


def compare_frames_change_detection(prev_frame, next_frame, min_contour_area):
    frame_delta = cv2.absdiff(prev_frame, next_frame)
    thresh = cv2.threshold(frame_delta, 45, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    score = 0
    res_cnts = []
    for c in cnts:
        if cv2.contourArea(c) < min_contour_area:
            continue

        res_cnts.append(c)
        score += cv2.contourArea(c)

    return score, res_cnts, thresh


def resize_image(image, desired_width, desired_height):
    if image is None or image.size == 0:  # Check if the image is empty
        return None
    return cv2.resize(image, (desired_width, desired_height))

def remove_similar_images(folder_path, threshold_score=5000, gaussian_blur_radius_list=[5], black_mask=(5, 10, 5, 0), desired_width=640, desired_height=480):
    # Get a list of image filenames in the folder
    image_filenames = [filename for filename in os.listdir(folder_path) if filename.endswith('.png')]

    # Sort the image filenames to ensure consistent order
    image_filenames.sort()

    # Convert the filenames to full paths
    image_paths = [os.path.join(folder_path, filename) for filename in image_filenames]

    # Load the images, resize them, and store them in a list
    images = [cv2.imread(image_path) for image_path in image_paths]
    resized_images = [resize_image(image, desired_width, desired_height) for image in images]

    # Filter out the None values (empty images)
    resized_images = [image for image in resized_images if image is not None]

    # List to store the indices of similar images to be removed
    images_to_remove = set()

    for i in range(len(resized_images) - 1):
        # Preprocess the images for comparison
        prev_processed = preprocess_image_change_detection(resized_images[i], gaussian_blur_radius_list, black_mask)

        for j in range(i + 1, len(resized_images)):
            # Skip already marked images
            if j in images_to_remove:
                continue

            # Preprocess the next image for comparison
            next_processed = preprocess_image_change_detection(resized_images[j], gaussian_blur_radius_list, black_mask)

            # Compare the images
            score, _, _ = compare_frames_change_detection(prev_processed, next_processed, min_contour_area=100)

            # Check if the score is below the threshold, indicating similarity
            if score < threshold_score:
                images_to_remove.add(j)  # Mark the next image to be removed

    # Remove the similar images from the folder
    for index in sorted(images_to_remove, reverse=True):
        os.remove(image_paths[index])

if __name__ == "__main__":
    folder_path = "D:\Kopernikus\dataset"
    
    threshold_score = 50000
    gaussian_blur_radius_list = [5]
    black_mask = (10, 15, 10, 0)
    desired_width = 640
    desired_height = 480

    remove_similar_images(folder_path, threshold_score, gaussian_blur_radius_list, black_mask, desired_width, desired_height)
