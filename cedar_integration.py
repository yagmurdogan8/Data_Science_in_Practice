import pandas as pd
import requests
import json

# Load your CSV file into a DataFrame
df = pd.read_csv('labeled_reports.csv')

# CEDAR API settings
cedar_api_url = "https://resource.metadatacenter.org/template-instances"
cedar_api_key = "8bda18e7a61832e5df3cb2878cf47cc334753467f06909d4b78d01c29504ddd8"

headers = {
    "Authorization": f"apiKey {cedar_api_key}",
    "Content-Type": "application/json"
}

# Loop through the CSV and prepare metadata entries
for index, row in df.iterrows():
    # Prepare a metadata instance
    metadata_instance = {
        "@context": "https://schema.metadatacenter.org/",
        "schema:isBasedOn": {
            "@id": "https://repo.metadatacenter.org/templates/1a2bc274-9a4e-44f3-b900-6f925c837fc8"
        },
        "schema:name": f"Instance {index + 1}",  # You can use a specific column here if you have a suitable one
        "Place": row['Place'],  
        "Perpetrator": row['Perpetrator'],
        "Date": row['Date'],
        "Gang violence": row['Gang violence: Yes/No'],
        "Sexual violence": row['Sexual violence: Yes/No'],
        "Famine": row['Famine: Yes/No'], 
        "Keywords": row['Keywords'], 
        "Text": row['Text']
    }

    # Send POST request to create instance in CEDAR
    response = requests.post(cedar_api_url, headers=headers, data=json.dumps(metadata_instance))

    if response.status_code == 201:
        print(f"Metadata instance created successfully for row {index}")
    else:
        print(f"Failed to create metadata instance for row {index}. Error: {response.text}")
