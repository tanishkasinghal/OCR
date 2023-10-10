import os
import requests

# Function to make an API call with the PDF file
def make_api_call(pdf_path):
    # Replace 'YOUR_API_ENDPOINT' with the actual API endpoint
    api_endpoint = 'http://localhost:8082/ocr/readImage'

    # Open the PDF file in binary mode and read its content
    with open(pdf_path, 'rb') as file:
        files = {'image': (os.path.basename(pdf_path), file, 'application/pdf')}
        response = requests.post(api_endpoint, files=files)
    print(response.text)
    return response.text

# Directory containing the PDF files
pdf_directory = '/home/tanishka/Documents/pdf-receipt-Generator/pdfs'

# Iterate over each file in the directory
file_count = 0
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)

        # Make API call with the PDF file
        api_response = make_api_call(pdf_path)
        file_count += 1
        if file_count == 10:
            print("Processed 10 files. Exiting.")
            break
