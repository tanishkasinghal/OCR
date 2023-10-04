import PyPDF2
import requests
import mysql.connector

def create_connection():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Admin123',
        database='ocr'
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

import re

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

if __name__ == "__main__":
    pdf_path = "aman_hospital.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    
    with open("extracted_text.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(extracted_text)
    
    print("Text extracted and saved to 'extracted_text.txt'\n")
    print(extracted_text)

    with open("extracted_text.txt", "r") as file:
        text = file.read()
    
    extracted_info = extract_info_from_text(text)
    # send_file_to_api(extracted_info)
    print(extracted_info)
