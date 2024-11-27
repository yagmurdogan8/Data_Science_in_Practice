from transformers import pipeline

# Step 1: Load the data
input_csv = "haiti_situation_reports_fetch.csv"
output_csv = "haiti_situation_reports_classified.csv"
df = pd.read_csv(input_csv)

# Step 2: Initialize pre-trained models
# Named Entity Recognition (NER) for Place, Date, etc.
ner_model = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

# Multi-label classification for event types, famine, migration, etc.
classification_model = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define classes for classification
classes = ["Migration", "Shootings", "Famine", "Sexual Violence", "Protests", "Gang Violence"]

# Step 3: Function to process and classify content
def classify_content(text):
    # Initialize result dictionary
    results = {"Place": "", "Date": "", "Who is involved": "", "Perpetrator": ""}

    # Perform NER to extract Place, Date, Who is involved
    ner_results = ner_model(text)
    for entity in ner_results:
        if entity["entity_group"] == "LOC":
            results["Place"] += entity["word"] + " "
        elif entity["entity_group"] == "PER":
            results["Who is involved"] += entity["word"] + " "
        elif entity["entity_group"] == "ORG" or entity["entity_group"] == "MISC":
            results["Perpetrator"] += entity["word"] + " "
        elif entity["entity_group"] == "DATE":
            results["Date"] += entity["word"] + " "

    # Perform multi-label classification for categories
    classification_results = classification_model(text, classes, multi_label=True)
    for label, score in zip(classification_results["labels"], classification_results["scores"]):
        results[label] = "Yes" if score > 0.5 else "No"

    return results

# Step 4: Process all content in the DataFrame
classified_data = []
for index, row in df.iterrows():
    print(f"Processing: {row['title']}")
    content = row["content"]
    if pd.isna(content) or content.strip() == "":
        classified_data.append({
            "title": row["title"],
            "url": row["url"],
            "Place": "",
            "Date": "",
            "Who is involved": "",
            "Perpetrator": "",
            "Migration": "No",
            "Shootings": "No",
            "Famine": "No",
            "Sexual Violence": "No",
            "Gang Violence": "No",
            "Protests": "No"
        })
    else:
        classifications = classify_content(content)
        classified_data.append({
            "title": row["title"],
            "url": row["url"],
            **classifications
        })

# Step 5: Save results to a CSV file
classified_df = pd.DataFrame(classified_data)
classified_df.to_csv(output_csv, index=False)
print(f"Classified data saved to {output_csv}")
