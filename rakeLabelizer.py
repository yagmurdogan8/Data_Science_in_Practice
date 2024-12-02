import re
import pandas as pd
import spacy
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from rake_nltk import Rake

# Initialize RAKE and spaCy
rake = Rake()
nlp = spacy.load("en_core_web_sm")

# Fine-tuned model path
MODEL_PATH = "./fine_tuned_model"

# Initialize the fine-tuned model pipeline
classifier = pipeline("text2text-generation", model=MODEL_PATH)

# Attributes to classify
ATTRIBUTES = ["Place", "Perpetrator", "Date", "Gang violence: Yes/No", "Sexual violence: Yes/No", "Famine: Yes/No"]

def preprocess_text(text):
    """Clean and preprocess the text."""
    text = re.sub(r"(http\S+|www\.\S+)", "", text)  # Remove URLs
    text = re.sub(r"\s+", " ", text)  # Normalize spaces
    return text.strip()

def extract_keywords(text):
    """Extract important keywords using RAKE."""
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()

def classify_with_fine_tuned_model(report):
    """Classify report using the fine-tuned model."""
    results = {}
    for attribute in ATTRIBUTES:
        prompt = f"Extract the {attribute} from the following situation:\n{report}"
        result = classifier(prompt, max_new_tokens=50)
        results[attribute] = result[0]['generated_text'].strip()
    return results

def classify_with_ner(report):
    """Classify report using spaCy NER."""
    doc = nlp(report)
    results = {"Place": "Unknown", "Perpetrator": "Unknown"}
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity
            results["Place"] = ent.text
        elif ent.label_ == "ORG":  # Organizations (may include perpetrators)
            results["Perpetrator"] = ent.text
    return results

def merge_results(fine_tuned_results, ner_results, keywords):
    """Combine results from fine-tuned model, NER, and RAKE."""
    combined_results = fine_tuned_results.copy()
    combined_results["Place"] = ner_results.get("Place", "Unknown")
    combined_results["Perpetrator"] = ner_results.get("Perpetrator", "Unknown")
    combined_results["Keywords"] = ", ".join(keywords)
    return combined_results

def process_report(report):
    """Process a single report and extract attributes."""
    report = preprocess_text(report)
    keywords = extract_keywords(report)
    ner_results = classify_with_ner(report)
    fine_tuned_results = classify_with_fine_tuned_model(report)
    return merge_results(fine_tuned_results, ner_results, keywords)

def process_reports(reports, output_file="labeled_reports.csv"):
    """Process multiple reports and save labeled results to a CSV file."""
    labeled_data = []
    for idx, report in enumerate(reports):
        print(f"Processing report {idx + 1}/{len(reports)}")
        attributes = process_report(report)
        attributes["Text"] = report
        labeled_data.append(attributes)

    # Save results to CSV
    df = pd.DataFrame(labeled_data)
    df.to_csv(output_file, index=False)
    print(f"Labeled reports saved to {output_file}")

# Example usage
if __name__ == "__main__":
    situation_reports = [
        "37 Haitian police officers were killed by criminals in 2023. This happened in Port-au-Prince.",
        "50 civilians fled Cap-Haïtien after gang violence erupted on 2023-11-15.",
        "A famine has been declared in rural areas, impacting thousands."
    ]
    process_reports(situation_reports)
