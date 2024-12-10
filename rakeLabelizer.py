import re
import pandas as pd
import spacy
from transformers import pipeline
from rake_nltk import Rake

# Initialize RAKE and spaCy
rake = Rake()
nlp = spacy.load("en_core_web_trf")  # Use the transformer-based model for better accuracy

# Fine-tuned model path
MODEL_PATH = "./fine_tuned_model"

# Initialize the fine-tuned model pipeline
classifier = pipeline("text2text-generation", model=MODEL_PATH)

# Attributes to classify
ATTRIBUTES = ["Place", "Perpetrator", "Date", "Gang violence", "Sexual violence", "Famine"]

# Keywords for conflict types
place_keywords = {
    "port-au-prince", "cite soleil", "cap-haïtien", "les cayes", "gonaïves", "jacmel", "hinche", "petionville"
}
perpetrator_keywords = {
    "gangs", "militants", "criminals", "marauders", "unknown", "economic hardship"
}
gang_violence_keywords = {"gangs", "violence", "marauders"}
sexual_violence_keywords = {"sexual violence", "assault", "rape", "harassment", "abuse"}
famine_keywords = {"famine", "hunger", "food scarcity", "starvation"}


def map_keywords_to_conflict_types(keywords):
    """Map extracted keywords to specific conflict types."""
    gang_violence = any(keyword.lower() in gang_violence_keywords for keyword in keywords)
    sexual_violence_detected = any(
        any(kw in keyword.lower() for kw in sexual_violence_keywords) for keyword in keywords
    )
    famine_detected = any(keyword.lower() in famine_keywords for keyword in keywords)
    
    return {
        "Gang violence": "Yes" if gang_violence else "No",
        "Sexual violence": "Yes" if sexual_violence_detected else "No",
        "Famine": "Yes" if famine_detected else "No"
    }


def map_keywords_to_attributes(keywords):
    """Map keywords to place and perpetrator attributes."""
    place = next((word for word in keywords if word.lower() in place_keywords), "Unknown")
    perpetrator = next((word for word in keywords if word.lower() in perpetrator_keywords), "Unknown")
    return {"Place": place, "Perpetrator": perpetrator}


def preprocess_text(text):
    """Clean and preprocess the text."""
    text = re.sub(r"(http\S+|www\.\S+)", "", text)  # Remove URLs
    text = re.sub(r"\s+", " ", text)  # Normalize spaces
    text = text.lower()  # Convert to lowercase for consistency
    return text.strip()


def extract_keywords(text):
    """Extract important keywords using RAKE."""
    rake.extract_keywords_from_text(text)
    keywords = rake.get_ranked_phrases()
    print(f"Extracted keywords: {keywords}")  # Debugging statement
    return keywords


def classify_with_ner(report):
    """Classify report using spaCy NER."""
    doc = nlp(report)
    results = {"Place": "Unknown", "Perpetrator": "Unknown"}
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical entity
            results["Place"] = ent.text
        elif ent.label_ in {"ORG", "NORP"}:  # Organizations or groups
            results["Perpetrator"] = ent.text
    return results


def classify_with_fine_tuned_model(report):
    """Classify report using the fine-tuned model."""
    results = {}
    for attribute in ATTRIBUTES:
        prompt = f"Extract the {attribute} from the following situation:\n{report}"
        result = classifier(prompt, max_new_tokens=50)
        results[attribute] = result[0]['generated_text'].strip()
    
    # Debugging fine-tuned model output
    print(f"Fine-tuned model results: {results}")
    
    # Map keywords for manual detection
    keywords = extract_keywords(report)
    mapped_conflicts = map_keywords_to_conflict_types(keywords)
    
    # Update the conflict categories detected by keyword mapping
    results.update(mapped_conflicts)
    return results


def merge_results(fine_tuned_results, ner_results, keywords):
    """Combine results from fine-tuned model, NER, and RAKE."""
    keyword_results = map_keywords_to_attributes(keywords)
    combined_results = fine_tuned_results.copy()
    combined_results["Place"] = ner_results.get("Place", keyword_results["Place"])
    combined_results["Perpetrator"] = ner_results.get("Perpetrator", keyword_results["Perpetrator"])
    combined_results["Keywords"] = ", ".join(keywords)
    return combined_results


def process_report(report):
    """Process a single report and extract attributes."""
    report = preprocess_text(report)
    keywords = extract_keywords(report)
    print(f"Keywords: {keywords}")  # Debug keywords
    ner_results = classify_with_ner(report)
    print(f"NER Results: {ner_results}")  # Debug NER results
    fine_tuned_results = classify_with_fine_tuned_model(report)
    print(f"Fine-Tuned Model Results: {fine_tuned_results}")  # Debug fine-tuned results
    merged_results = merge_results(fine_tuned_results, ner_results, keywords)
    print(f"Merged Results: {merged_results}")  # Debug merged results
    return merged_results


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


if __name__ == "__main__":
    input_file = "fake_situation_reports.csv"
    output_file = "labeled_reports.csv"

    # Read the CSV file and extract the "Text" column
    df = pd.read_csv(input_file)
    if "Text" not in df.columns:
        raise ValueError(f"The input file {input_file} does not contain a 'Text' column.")

    reports = df["Text"].tolist()  # Extract the list of reports
    process_reports(reports, output_file=output_file)
