import cv2
import pytesseract
import numpy as np

# Load the image
image = cv2.imread('images/aman_hospital_page-0001.jpg')

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image
_, im_bw = cv2.threshold(gray_image, 150, 150, cv2.THRESH_BINARY)

# Perform OCR to extract printed text
printed_text = pytesseract.image_to_string(im_bw)

# Apply edge detection to identify handwritten regions
edges = cv2.Canny(gray_image, threshold1=30, threshold2=100)  # Adjust thresholds as needed

# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize a list to store handwritten regions
handwritten_regions = []

# Define a threshold for identifying handwritten regions based on contour area
min_contour_area = 1000  # Adjust as needed

# Iterate through contours and identify handwritten regions
for contour in contours:
    if cv2.contourArea(contour) > min_contour_area:
        x, y, w, h = cv2.boundingRect(contour)
        handwritten_region = image[y:y+h, x:x+w]
        handwritten_regions.append(handwritten_region)

# Save handwritten regions as separate images
for idx, region in enumerate(handwritten_regions):
    cv2.imwrite(f"temp/handwritten_{idx}.jpg", region)

# Print or process the extracted printed text
print("Printed Text:")
print(printed_text)
