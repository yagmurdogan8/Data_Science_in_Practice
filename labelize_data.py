import re
import csv
import os
from PyPDF2 import PdfReader

def extract_metadata_from_text(text):
    metadata = {
        "date": None,
        "people_involved": [],
        "type_of_situation": None,
        "key_points": []
    }
    
    # Extract date in the format "26 June 2024"
    date_match = re.search(r"\b(\d{1,2}\s[A-Za-z]+\s\d{4})\b", text)
    if date_match:
        metadata["date"] = date_match.group(1)
    
    # Extract proper names (filter noise)
    people_matches = re.findall(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b", text)
    common_noise = {"Haiti Matters", "United Nations", "Food and Agriculture Organization", "Médecins Sans Frontières"}
    metadata["people_involved"] = [name for name in set(people_matches) if name not in common_noise]
    
    # Identify type of situation by keywords
    if "gang violence" in text.lower():
        metadata["type_of_situation"] = "Gang Violence"
    elif "humanitarian aid" in text.lower():
        metadata["type_of_situation"] = "Humanitarian Aid"
    elif "political crisis" in text.lower():
        metadata["type_of_situation"] = "Political Crisis"
    
    # Extract bullet points or short paragraphs as key points
    bullets = re.findall(r"[-•]\s+(.*?)(?:\n|$)", text)
    metadata["key_points"] = [point.strip() for point in bullets if len(point.split()) > 3]
    
    return metadata

def process_pdf(file_path):
    reader = PdfReader(file_path)
    text = " ".join(page.extract_text() for page in reader.pages)
    return extract_metadata_from_text(text)

def process_reports(input_dir, output_file):
    all_data = []
    
    # Iterate through all PDF files in the directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(input_dir, file_name)
            print(f"Processing: {file_name}")
            metadata = process_pdf(file_path)
            all_data.append(metadata)
    
    # Write results to a CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["date", "people_involved", "type_of_situation", "key_points"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
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
    input_directory = "situtation reports"  
    output_csv = "situation_reports_refined.csv"
    process_reports(input_directory, output_csv)
