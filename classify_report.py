from transformers import pipeline

# Step 1: Multi-task structured classification
def classify_report(report_text, model_path="./fine_tuned_model"):
    # Load the fine-tuned model and tokenizer
    classifier = pipeline("text2text-generation", model=model_path)

    # Define attributes to classify
    attributes = [
        "Place", 
        "Perpetrator", 
        "Date", 
        "Gang violence: Yes/No", 
        "Sexual violence: Yes/No", 
        "Famine: Yes/No"
    ]
    
    # Classify each attribute
    results = {}
    for attribute in attributes:
        prompt = f"Extract the {attribute} from the following situation report:\n{report_text}"
        result = classifier(prompt, max_new_tokens=50)  # Allow enough space for the output
        results[attribute] = result[0]['generated_text'].strip()

    return results

# Example: Classify a new situation report
if __name__ == "__main__":
    new_report = """
    37 Haitian police officers were killed by criminals in 2023. The loss of police officers on the force has significantly reduced the effectiveness of the National Police Forces. """

    print("Classifying new report...")
    classification_results = classify_report(new_report)
    print("Classification Results:")
    for key, value in classification_results.items():
        print(f"{key}: {value}")
    print("Classification completed.")
