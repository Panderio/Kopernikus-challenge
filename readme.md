# Image Similarity Detection Project

## Overview

This project aims to detect and remove similar images from a dataset collected from multiple cameras. The goal is to identify duplicate or nearly identical images, which can help in reducing storage requirements and streamline further image processing tasks. The project utilizes image processing techniques to compare frames and eliminate redundant content.

## Table of Contents

- [Introduction](#introduction)
- [Project Files](#project-files)
- [Dataset Overview](#dataset-overview)
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

---

_This is an AI-generated readme template for the "Image Similarity Detection Project." The actual content and details may vary based on the project's specific requirements and data._