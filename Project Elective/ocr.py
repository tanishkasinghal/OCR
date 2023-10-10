import cv2
from PIL import Image
import pytesseract
im_file="page_01.jpg"
im=Image.open(im_file)
print(im)
# im.show()
# im.rotate(90).show()
# im.save("tem_page_01.jpg")