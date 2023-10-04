
import logging as logger
import mysql.connector
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
        db_patterns = get_regex_patterns_from_db()
        if filename.endswith('.pdf'):
            pdf_path = os.path.join('uploads', filename)
            extracted_text = extract_text_from_pdf(pdf_path)
            extracted_info = extract_info_from_text(extracted_text,db_patterns)
            send_file_to_api(extracted_info)
            return jsonify({'message': 'File successfully uploaded and processed.'})
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = os.path.join('uploads', filename)
            extracted_text = extract_text_from_image(image_path)
            extracted_info = extract_info_from_text(extracted_text,db_patterns)
            send_file_to_api(extracted_info)
            return jsonify({'message': 'Image uploaded. Processing logic not implemented.'})
        else:
            return 'Invalid file type'

    else:
        return 'Invalid file type'

def create_connection():
    # Connect to the MySQL database (hosted locally)
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Admin@123',
        database='dictionary'
    )
    return conn

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

def extract_info_from_text(text, db_patterns):
    #print(db_patterns)
    info = {}

    for pattern in db_patterns:
        fieldname = pattern["fieldname"]
        # regex_pattern = pattern["pattern"]
        initial_pattern = pattern["pattern"]

        # Appending ": (.+)" to the existing regex pattern
        if fieldname in {'name', 'sex'}:
            regex_pattern = initial_pattern + r'\s*:\s*(.+)'
        elif fieldname in {'age','contact'}:
            regex_pattern = initial_pattern + r'\s*:\s*(\d+)'
        else:
            regex_pattern = initial_pattern + r'\s*:\s*((?:.*\n)*.*\))\s*'

        match = re.search(regex_pattern, text, re.IGNORECASE)
        if match:
            info[fieldname] = match.group(1).strip()
    #print(info)
    return info

def get_regex_patterns_from_db():
    db_patterns = []
    connection = None

    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute a SELECT query to retrieve regex patterns from the database
        cursor.execute("SELECT fieldname, pattern FROM ocr_dict")

        # Fetch all rows as a list of dictionaries
        db_patterns = cursor.fetchall()

    except mysql.connector.Error as e:
        print(f"MySQL error: {e}")

    finally:
        if connection:
            connection.close()

    return db_patterns


def send_file_to_api(data):
    url = 'http://localhost:8082/ocr/'
    headers = {'Content-Type': 'application/json'}
    patient_json = {
        "name": data.get("name"),
        "age": data.get("age"),
        "contact": data.get("contact"),
        "sex": data.get("sex"),
        "address": data.get("address")
    }
    print(patient_json)
    response = requests.post(url, json=patient_json, headers=headers)

    
if __name__ == '__main__':
    logger.debug("Starting Flask Server")
    # from api import *
    flaskAppInstance.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)