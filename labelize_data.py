import os
import re
import csv
import pandas as pd
from transformers import pipeline
import spacy
from PyPDF2 import PdfReader

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")

# Load BERT for text classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define categories for classification
CATEGORIES = ["Gang Violence", "Humanitarian Aid", "Political Crisis", "Food Security"]

def extract_entities_and_classify(text):
    metadata = {
        "date": None,
        "people_involved": [],
        "organizations": [],
        "type_of_situation": None,
        "key_points": []
    }
    
    # Extract date
    date_match = re.search(r"\b(\d{1,2}\s[A-Za-z]+\s\d{4})\b", text)
    if date_match:
        metadata["date"] = date_match.group(1)
    
    # Use spaCy for NER
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            metadata["people_involved"].append(ent.text)
        elif ent.label_ == "ORG":
            metadata["organizations"].append(ent.text)
    
    # Deduplicate lists
    metadata["people_involved"] = list(set(metadata["people_involved"]))
    metadata["organizations"] = list(set(metadata["organizations"]))
    
    # Extract bullet points for key points
    bullets = re.findall(r"[-•]\s+(.*?)(?:\n|$)", text)
    metadata["key_points"] = [point.strip() for point in bullets if len(point.split()) > 3]
    
    # Use BERT-based classifier for type of situation
    classification = classifier(text, CATEGORIES)
    metadata["type_of_situation"] = classification["labels"][0]  # Top category
    
    return metadata

def process_pdf(file_path):
    reader = PdfReader(file_path)
    text = " ".join(page.extract_text() for page in reader.pages)
    return extract_entities_and_classify(text)

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
        fieldnames = ["date", "people_involved", "organizations", "type_of_situation", "key_points"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_data:
            writer.writerow({
                "date": data["date"],
                "people_involved": ", ".join(data["people_involved"]),
                "organizations": ", ".join(data["organizations"]),
                "type_of_situation": data["type_of_situation"],
                "key_points": "; ".join(data["key_points"])
            })
    
    print(f"Data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    input_directory = "situtation reports"  
    output_csv = "situation_reports_with_ner.csv"
    process_reports(input_directory, output_csv)
