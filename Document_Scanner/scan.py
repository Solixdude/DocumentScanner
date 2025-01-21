from transform import four_point_transform
from skimage.filters import threshold_local
import argparse
import cv2
import imutils

# Setup argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image to be scanned")
args = vars(ap.parse_args())

# Load the image and preprocess
image = cv2.imread(args["image"])
if image is None:
    raise FileNotFoundError(f"Image not found at path: {args['image']}")

ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)

# Convert to grayscale, blur, and detect edges
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Adjust Canny thresholds
lower_threshold = 50
upper_threshold = 150
edged = cv2.Canny(gray, lower_threshold, upper_threshold)

# Show the edges for debugging
print("STEP 1: Edge Detection")
cv2.imshow("Edges", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Find contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Sort contours by area and keep only significant ones
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# Debug: Draw all detected contours
debug_image = image.copy()
cv2.drawContours(debug_image, cnts, -1, (0, 255, 0), 2)
cv2.imshow("All Contours", debug_image)
cv2.waitKey(0)

# Approximate the screen contour
screenCnt = None
for c in cnts:
    if cv2.contourArea(c) < 5000:  # Ignore small contours
        continue

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    print(f"Detected contour with {len(approx)} points.")

    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    raise ValueError("No contour with four points was found. Try adjusting parameters or preprocessing the image.")

# Draw the contour
print("STEP 2: Find contours of paper")
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perspective transform
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

# Apply thresholding
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset=10, method="gaussian")
warped = (warped > T).astype("uint8") * 255

# Show the result
print("STEP 3: Apply perspective transform")
cv2.imshow("Original", imutils.resize(orig, height=650))
cv2.imshow("Scanned", imutils.resize(warped, height=650))
cv2.waitKey(0)
