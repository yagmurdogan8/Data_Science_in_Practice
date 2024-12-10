import random

# List of sample locations and events for generating fake reports
places = [
    "Port-au-Prince", "Cap-Haïtien", "Les Cayes", "Gonaïves", "Jacmel", "Hinche", "Petionville", "Cite Soleil"
]
perpetrators = [
    "gangs", "criminals", "unknown", "militants", "marauders", "economic hardship", "natural disaster"
]
events = [
    "violence", "famine", "economic instability", "healthcare crisis", "gang disputes", "protests", "police conflicts"
]
dates = [
    "2022-01-15", "2023-11-20", "2023-07-10", "2023-06-15", "2022-12-05", "2023-09-25", "2023-10-30"
]

# Function to generate random fake reports
def generate_fake_reports(num_reports):
    fake_reports = []
    for _ in range(num_reports):
        location = random.choice(places)
        perpetrator = random.choice(perpetrators)
        event = random.choice(events)
        date = random.choice(dates)
        
        # Create the fake report text
        report_text = f"{random.randint(10, 100)} people were affected by {event} in {location} on {date} due to {perpetrator}."
        fake_reports.append(report_text)
    return fake_reports

# Generate 100 fake reports
num_fake_reports = 100
fake_reports = generate_fake_reports(num_fake_reports)

# Output fake reports to a CSV-like structure for simulation
import pandas as pd

data = {
    "Text": fake_reports,
    "Place": [random.choice(places) for _ in range(num_fake_reports)],
    "Perpetrator": [random.choice(perpetrators) for _ in range(num_fake_reports)],
    "Date": [random.choice(dates) for _ in range(num_fake_reports)],
    "Gang violence": random.choices(["Yes", "No"], k=num_fake_reports),
    "Sexual violence": random.choices(["Yes", "No"], k=num_fake_reports),
    "Famine": random.choices(["Yes", "No"], k=num_fake_reports)
}

fake_df = pd.DataFrame(data)

# Save to CSV
fake_df.to_csv("fake_situation_reports.csv", index=False)
print("100 fake reports generated and saved to 'fake_situation_reports.csv'")
