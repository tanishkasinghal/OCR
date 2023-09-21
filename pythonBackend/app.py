
import logging as logger

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import PyPDF2
import re
import requests
from PIL import Image
import cv2
import pytesseract

logger.basicConfig(level="DEBUG")

flaskAppInstance = Flask(__name__)  

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@flaskAppInstance.route('/upload', methods=['POST'])
def upload_file():
    print("aya")
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        
        if filename.endswith('.pdf'):
            # If it's a PDF, extract text and send data to another API
            pdf_path = os.path.join('uploads', filename)
            extracted_text = extract_text_from_pdf(pdf_path)
            extracted_info = extract_info_from_text(extracted_text)
            send_file_to_api(extracted_info)
            
            return jsonify({'message': 'File successfully uploaded and processed.'})
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join('uploads', filename)
            extracted_text = extract_text_from_image(image_path)
            extracted_info = extract_info_from_text(extracted_text)
            send_file_to_api(extracted_info)
            return jsonify({'message': 'Image uploaded. Processing logic not implemented.'})
        else:
            return 'Invalid file type'

    else:
        return 'Invalid file type'

def extract_text_from_pdf(pdf_path):
    text = ""
    
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
            
    return text

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, im_bw = cv2.threshold(gray_image, 150, 150, cv2.THRESH_BINARY)
    extracted_text = pytesseract.image_to_string(im_bw)
    return extracted_text

def extract_info_from_text(text):
    info = {}
    
    # Extract Name
    name_pattern = r"Name: (.+)"
    name_match = re.search(name_pattern, text)
    if name_match:
        info["Name"] = name_match.group(1)
    
    # Extract Age
    age_pattern = r"Age : (\d+)"
    age_match = re.search(age_pattern, text)
    if age_match:
        info["Age"] = int(age_match.group(1))
    
    # Extract Mobile Number
    mobile_pattern = r"Mobile No : (\d+)"
    mobile_match = re.search(mobile_pattern, text)
    if mobile_match:
        info["Mobile"] = mobile_match.group(1)
    
    # Extract Sex
    sex_pattern = r"Sex : (.+)"
    sex_match = re.search(sex_pattern, text)
    if sex_match:
        info["Sex"] = sex_match.group(1)
    
    # Extract Address
    address_pattern = r"Address :((?:.*\n)*.*\))\s*"
    address_match = re.search(address_pattern, text)
    if address_match:
        address = address_match.group(1).strip()
        info["Address"] = address
    
    return info


def send_file_to_api(data):
    url = 'http://localhost:8082/ocr/'
    headers = {'Content-Type': 'application/json'}
    patient_json = {
        "name": data.get("Name"),
        "age": data.get("Age"),
        "contact": data.get("Mobile"),
        "sex": data.get("Sex"),
        "address": data.get("Address")
    }
    
    response = requests.post(url, json=patient_json, headers=headers)

    
if __name__ == '__main__':
    logger.debug("Starting Flask Server")
    # from api import *
    flaskAppInstance.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)