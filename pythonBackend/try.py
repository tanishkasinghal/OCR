import re

text = """Address :Kahira Garh, KHAIRGARH CHHUIKHADAN 
GANDAI(CHHATTISGARH)"""

regex_pattern = r'address\s*:\s*(.*?)(?=\w+\s*:|\Z)'
match = re.search(regex_pattern, text, re.IGNORECASE)

if match:
    residence_info = match.group(1)
    print(residence_info)
else:
    print("No match found.")
