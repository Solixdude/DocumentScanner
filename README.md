Document Scanner

This project is a simple document scanner that uses image processing techniques to detect and transform a document from an image into a top-down, scanned-like view.

Features

Detects document edges in an image.

Applies a four-point perspective transform to get a "scanned" version of the document.

Converts the scanned image into a binarized format for a cleaner output.

Files

1. scan.py

This is the main script that handles:

Loading the input image.

Preprocessing (grayscale conversion, Gaussian blur, edge detection).

Detecting the document contour.

Applying a perspective transform and thresholding for the final scanned result.

2. transform.py

This file contains helper functions for:

Ordering the points of a contour to ensure consistent transformations.

Applying a four-point perspective transform to an image.

Dependencies

The following Python libraries are required:

numpy

opencv-python

imutils

scikit-image

Install them using pip:

pip install numpy opencv-python imutils scikit-image

Usage

Run the script using the following command:

python scan.py --image path_to_image

Example

python scan.py --image example.jpg

The script will:

Display the detected edges.

Highlight the detected document contour.

Show the final scanned image.

How It Works

Edge Detection:

The input image is resized, converted to grayscale, blurred, and edges are detected using the Canny algorithm.

Contour Detection:

The script finds the largest contours in the image and identifies the one that has four points, assuming it's the document.

Perspective Transform:

Using the four detected points, the perspective of the image is transformed to obtain a top-down view.

Thresholding:

The transformed image is binarized using adaptive thresholding for a clean, scanned appearance.

Debugging Tips

Ensure the input image has good lighting and clear document edges.

Adjust the Canny edge detection thresholds if no edges are detected.

Use the debug visualization steps in the script to inspect intermediate results.


License

This project is licensed under the MIT License.
