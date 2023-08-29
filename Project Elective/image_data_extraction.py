import cv2
import pytesseract
image = cv2.imread('image.jpeg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

extracted_text = pytesseract.image_to_string(gray_image)
# Print or process extracted text
print(extracted_text)
