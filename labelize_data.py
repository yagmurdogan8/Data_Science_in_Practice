import re
import os
import csv
import glob
from PyPDF2 import PdfReader

def extract_metadata_from_pdf(file_path):
    metadata = {
        "date": None,
        "people_involved": [],
        "type_of_situation": None,
        "key_points": []
    }
    
    # Read the content of the PDF
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    # Extract metadata
    # Example: Extract date
    date_match = re.search(r"(\d{1,2} [A-Za-z]+ \d{4})", text)
    if date_match:
        metadata["date"] = date_match.group(0)
    
    # Example: Extract people involved (basic regex for names)
    people_match = re.findall(r"[A-Z][a-z]+\s[A-Z][a-z]+", text)
    if people_match:
        metadata["people_involved"] = list(set(people_match))  # Deduplicate names
    
    # Example: Extract situation type keywords (customize as needed)
    if "gang violence" in text.lower():
        metadata["type_of_situation"] = "Gang Violence"
    elif "humanitarian aid" in text.lower():
        metadata["type_of_situation"] = "Humanitarian Aid"
    elif "political crisis" in text.lower():
        metadata["type_of_situation"] = "Political Crisis"
    
    # Example: Extract key points (customize as needed)
    bullet_points = re.findall(r"- ([^\n]+)", text)
    if bullet_points:
        metadata["key_points"] = bullet_points
    
    return metadata

def process_reports(directory, output_file):
    all_data = []
    
    # Iterate through all PDF files in the directory
    for file_path in glob.glob(os.path.join(directory, "*.pdf")):
        print(f"Processing: {file_path}")
        metadata = extract_metadata_from_pdf(file_path)
        all_data.append(metadata)
    
    # Write data to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "people_involved", "type_of_situation", "key_points"])
        writer.writeheader()
        for data in all_data:
            writer.writerow({
                "date": data["date"],
                "people_involved": ", ".join(data["people_involved"]),
                "type_of_situation": data["type_of_situation"],
                "key_points": "; ".join(data["key_points"])
            })

    print(f"Data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    directory = "path_to_your_pdf_reports"  # Change this to the folder containing your PDFs
    output_file = "situation_reports.csv"
    process_reports(directory, output_file)
