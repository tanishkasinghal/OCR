import mysql.connector
import PyPDF2
import requests
import re

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

# Example usage
if __name__ == "__main__":
    pdf_path = "/home/tanishka/Pictures/tanihska_singhal.png"
    extracted_text = extract_text_from_pdf(pdf_path)
    
    with open("extracted_text.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(extracted_text)
    
    print("Text extracted and saved to 'extracted_text.txt'\n")
    print(extracted_text)

    with open("extracted_text.txt", "r") as file:
        text = file.read()

    db_patterns = get_regex_patterns_from_db()
    
    extracted_info = extract_info_from_text(text, db_patterns)
    # send_file_to_api(extracted_info)
    print(extracted_info)
