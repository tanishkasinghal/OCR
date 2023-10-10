import requests
import os

# API endpoint URL
api_url = "https://localhost:8082/ocr/readImage"

# Directory containing your PDF files
pdf_directory = "/home/tanishka/Documents/pdf-receipt-Generator/pdfs"

def process_pdf(file_path):
    # Implement logic to read and process the PDF file
    # You may need to customize this part based on your API requirements
    print(f"Processing file: {file_path}")
    with open(file_path, 'rb') as file:
        files = {file_path: file}

        response = requests.post(api_url, files=files, verify=False)


        # Process the API response
        if response.status_code == 200:
            print(f"Successfully processed {file_path}")
            # Additional processing if needed
        else:
            print(f"Failed to process {file_path}. Status code: {response.status_code}")
            # Print or log the error message
            print(response.text)

def main():
    file_count = 0
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_directory, filename)
            process_pdf(file_path)

            file_count += 1
            if file_count == 10:
                print("Processed 10 files. Exiting.")
                break

if __name__ == "__main__":
    main()
