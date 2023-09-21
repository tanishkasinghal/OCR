import cv2
import pytesseract
image = cv2.imread('images/aman_hospital_page-0001.jpg')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# extracted_text = pytesseract.image_to_string(gray_image)


thresh, im_bw = cv2.threshold(gray_image, 150, 150, cv2.THRESH_BINARY)

# new_img=cv2.imwrite("temp/bw_image.jpg", im_bw)

extracted_text = pytesseract.image_to_string(im_bw)


# Print or process extracted text
print(extracted_text)
