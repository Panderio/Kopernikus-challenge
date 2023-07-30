# Image Similarity Detection Project

## Overview

This project aims to detect and remove similar images from a dataset collected from multiple cameras. The goal is to identify duplicate or nearly identical images, which can help in reducing storage requirements and streamline further image processing tasks. The project utilizes image processing techniques to compare frames and eliminate redundant content.

## Table of Contents

- [Introduction](#introduction)
- [Project Files](#project-files)
- [Dataset Overview](#dataset-overview)
- [Questions](#questions)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

With the increasing availability of surveillance cameras and other imaging devices, large datasets of images are becoming common. Such datasets often contain many duplicate or very similar images captured over time, resulting in unnecessary redundancy. This project offers an automated solution to detect and remove similar images from a dataset collected from multiple cameras.

## Project Files

This project consists of the following files:

1. `challenge_interview.py`: This is the main file that handles the comparison and removal of similar images. It utilizes multithreading for parallel processing to improve performance.

2. `imaging_interview.py`: This file contains image processing functions used in the main script. It includes functions for drawing color masks, preprocessing images, and comparing frames for change detection.

3. `image_utils.py`: This file contains utility functions used for working with image files, such as extracting camera IDs and timestamps, resizing images, and grouping images by camera ID.

## Dataset Overview

The dataset provided for this project contains images from four different cameras: c10, c20, c21, and c23. Each camera captures images at various time intervals. The key characteristics of each camera's dataset are as follows:

1. Camera c10:
   - Number of Images: 126
   - Average Time Between Images: 5 minutes and 45 seconds
   - Image Resolution: Mostly 640 x 480
   - Notes: Some images have outlier timestamps (26 seconds, 44 seconds, 1 minute and 2 seconds, and 18 minutes and 49 seconds). Additionally, a few images have an average time interval of approximately 6 minutes.

2. Camera c20:
   - Number of Images: 324
   - Average Time Between Images: 5 minutes
   - Image Resolution: Mostly 1920 x 1080
   - Notes: Some images have minor variations in timestamps, resulting in occasional noise.

3. Camera c21:
   - Number of Images: 146
   - Average Time Between Images: 5 minutes
   - Image Resolution: Mostly 1920 x 1080
   - Notes: Some images have outlier timestamps, and there is an image ("c21_2021_03_27__10_36_36") that cannot be opened. Additionally, an image ("c21_2021_03_27__12_53_37") has unusually small dimensions (10 x 6).

4. Camera c23:
   - Number of Images: 484
   - Average Time Between Images: 5 minutes and 43 seconds
   - Image Resolution: Mostly 1920 x 1080
   - Notes: Some images have noise with small intervals (42 seconds), and one image has a timestamp indicating a gap of approximately 2 to 3 days.

## Questions

**1. What did you learn after looking at our dataset?**

After analyzing the dataset provided, I observed that it contains images from four different cameras, namely c10, c20, c21, and c23. Each camera's dataset exhibits distinct characteristics in terms of the number of images, average time intervals between images, and image resolutions. Camera c10 has 126 images with an average time interval of approximately 5 minutes and 45 seconds, mostly with a resolution of 640 x 480. Camera c20 has 324 images captured at an average time interval of 5 minutes and primarily with a resolution of 1920 x 1080. Camera c21 contains 146 images with an average time interval of 5 minutes and mostly having a resolution of 1920 x 1080. However, it includes an image ("c21_2021_03_27__10_36_36") that cannot be opened and an image ("c21_2021_03_27__12_53_37") with unusually small dimensions of 10 x 6. Camera c23 comprises 484 images with an average time interval of about 5 minutes and 43 seconds, mainly having a resolution of 1920 x 1080. Some images in this dataset have small intervals (e.g., 42 seconds), and one image indicates a significant gap of approximately 2 to 3 days.

**2. How does your program work?**

The program follows a multithreaded approach to efficiently process images from each camera. It utilizes three main files:

- `imaging_interview.py`: Contains image processing functions, such as drawing color masks, preprocessing images, and comparing frames for change detection.

- `image_utils.py`: Provides utility functions to work with image files, including extracting camera IDs and timestamps, resizing images, and grouping images by camera ID.

- `challenge_interview.py`: The main file orchestrating the entire process. It starts by grouping images by camera ID using the utility functions. For each camera's image group, it performs the following steps:
  - Selects a reference image to start the comparison process.
  - Preprocesses the reference image for change detection using the `preprocess_image_change_detection` function.
  - Compares the reference image with other images in the group by preprocessing each image similarly.
  - Calculates the score and contour areas of differences between the reference and other images using the `compare_frames_change_detection` function.
  - Based on the score and specified threshold, identifies and removes similar images from the dataset.

**3. What values did you decide to use for input parameters, and how did you find these values?**

For this project, the input parameters chosen are:

- `threshold_score`: The threshold score determines the similarity threshold for removing similar images. I experimented with different values to strike a balance between removing true duplicates and retaining potentially relevant but similar images.

- `gaussian_blur_radius_list`: This list contains radii for Gaussian blur applied during image preprocessing. The values help in reducing noise and smooth out the image for better comparison. I selected a value of [5] after trying out various radii.

- `black_mask`: This parameter defines the percentage of black mask borders around the image, which helps eliminate irrelevant regions. I used the values (5, 10, 5, 0) to create a black mask around the image edges while preserving the central region.

The selection of these values was based on experimentation and observation of the dataset. I adjusted the parameters to achieve the best results in terms of accurately detecting similar images while avoiding the loss of potentially unique images.

**4. What would you suggest implementing to improve data collection of unique cases in the future?**

To improve data collection of unique cases in the future, the following suggestions can be considered:

- Timestamp Standardization: Implementing a consistent timestamp format across all cameras can aid in the proper organization and comparison of images.

- Quality Control: Conduct regular quality checks to ensure all images are correctly captured, and there are no corrupted or unreadable images in the dataset.

- Manual Verification: Conduct manual verification and labeling of images to identify any false positives or negatives generated by the automated image similarity detection process.

**5. Any other comments about your solution?**

No

## Installation

To run this project, you need Python installed on your system along with the following libraries:

- OpenCV (cv2)
- imutils

You can install the required libraries using the following commands:

```bash
pip install opencv-python
pip install imutils
```

## Usage

1. Clone this repository to your local machine.
2. Place the provided dataset folder containing images in the same directory as the project files.
3. Open the `challenge_interview.py` file and adjust the `folder_path`, `threshold_score`, `gaussian_blur_radius_list`, and `black_mask` parameters as needed.
4. Run the `challenge_interview.py` script using the following command:

```bash
python challenge_interview.py
```

5. The script will process the images from each camera, identify similar images, and remove redundant content based on the specified criteria.

## Contributing

If you wish to contribute to this project or report any issues, please feel free to open a new issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE). You are free to modify and distribute the code as per the terms of the license.
