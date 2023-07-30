import threading
from concurrent.futures import ThreadPoolExecutor
from imaging_interview import *
from image_utils import *


def process_camera_images(camera_id, images, target_width, target_height, threshold_score, gaussian_blur_radius_list, black_mask, lock):
    logger = logging.getLogger(__name__)
    logger.info(f"Processing images from camera {camera_id} - There are {len(images)} images.")

    images_to_remove = set()

    # Start with the first image as a reference
    reference_index = 0
    while reference_index < len(images):
        reference_image_path = images[reference_index]
        reference_image = cv2.imread(os.path.join(folder_path, reference_image_path))
        reference_image = resize_image(reference_image, target_width, target_height)

        if reference_image is None:
            logger.warning(f"Failed to read image {reference_image_path}. Skipping.")
            reference_index += 1
            continue

        # Preprocess the reference image for comparison
        reference_processed = preprocess_image_change_detection(reference_image, gaussian_blur_radius_list, black_mask)

        # Compare the reference image with the rest
        for i in range(reference_index + 1, len(images)):
            next_image_path = images[i]
            next_image = cv2.imread(os.path.join(folder_path, next_image_path))
            next_image = resize_image(next_image, target_width, target_height)
            if next_image is None:
                continue

            # Check the timestamp difference between the reference image and the next image
            reference_timestamp = parse_timestamp(get_timestamp(os.path.basename(reference_image_path)))
            next_timestamp = parse_timestamp(get_timestamp(os.path.basename(next_image_path)))

            time_difference = abs(next_timestamp - reference_timestamp)

            # Preprocess the next image for comparison
            next_processed = preprocess_image_change_detection(next_image, gaussian_blur_radius_list, black_mask)

            # Compare the images
            score, _, _ = compare_frames_change_detection(reference_processed, next_processed, min_contour_area=500)

            if score < threshold_score or time_difference < 150000:
                images_to_remove.add(next_image_path)  # Mark the next image for removal

        # Remove the similar images from the folder
        for image_path in images_to_remove:
            logger.info(f"Removing similar image: {image_path}")
            with lock:
                try:
                    os.remove(os.path.join(folder_path, image_path))
                except FileNotFoundError:
                    logger.warning(f"File {image_path} already removed. Skipping.")

        # Update the reference index to the next non-removed image
        reference_index += 1
        while reference_index < len(images) and images[reference_index] in images_to_remove:
            reference_index += 1

def remove_similar_images_parallel(folder_path, threshold_score=5000, gaussian_blur_radius_list=[5], black_mask=(5, 10, 5, 0)):
    logger = setup_logging()
    # Group images by camera ID
    camera_images = group_images_by_camera_id(folder_path)
    # Determine target size for each camera based on its resolution
    target_sizes = {camera_id: get_camera_resolution(camera_id) for camera_id in camera_images.keys()}
    lock = threading.Lock()


    with ThreadPoolExecutor() as executor:
        futures = []
        for camera_id, images in camera_images.items():
            target_width, target_height = target_sizes[camera_id]
            futures.append(executor.submit(process_camera_images, camera_id, images, target_width, target_height,
                                           threshold_score, gaussian_blur_radius_list, black_mask, lock))

        for future in futures:
            future.result()

if __name__ == "__main__":
    folder_path = "D:/Kopernikus/dataset"

    threshold_score = 20000  # Experiment with different values
    gaussian_blur_radius_list = [5]
    black_mask = (5, 10, 15, 0)
    remove_similar_images_parallel(folder_path, threshold_score, gaussian_blur_radius_list, black_mask)
