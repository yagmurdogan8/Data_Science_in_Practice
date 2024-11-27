# Step 6: Classify a New Report
def classify_new_report(new_report_text, title, url):
    # Classify the new report
    classifications = classify_content(new_report_text)

    # Add metadata
    new_report_data = {
        "title": title,
        "url": url,
        **classifications
    }

    return new_report_data

# Example new report text, title, and URL
new_report_text = """
Haiti is currently experiencing a severe escalation in gang-related violence, leading to widespread instability, 
significant loss of life, and a deepening humanitarian crisis. Below is a detailed overview of recent events, 
key actors, and affected regions:

Key Events and Incidents:

1. Pont-Sondé Massacre (October 3, 2024):
   Location: Pont-Sondé, Artibonite Department.
   Perpetrators: Gran Grif gang.
   Details: The Gran Grif gang launched a brutal attack on the town, resulting in at least 115 deaths and over 50 injuries. 
   The assailants used automatic rifles and knives, targeting civilians indiscriminately. Additionally, 45 houses and 
   34 vehicles were set ablaze, causing mass displacement.

2. Attempted Assault on Petion-Ville (November 19, 2024):
   Location: Petion-Ville, a suburb of Port-au-Prince.
   Perpetrators: Suspected gang members.
   Details: Over two dozen suspected gang members were killed when residents, alongside police forces, repelled an 
   attempted attack on the affluent suburb. Residents armed with machetes and hammers barricaded streets, leading 
   to the deaths of at least 25 individuals, some of whom were set on fire under burning tires.

3. UN Staff Evacuation (November 26, 2024):
   Location: Port-au-Prince.
   Details: The United Nations began evacuating staff due to escalating gang violence, with armed groups expanding 
   control over the capital. Humanitarian flights were organized to relocate officials, highlighting the deteriorating 
   security situation.

4. "Killdozer" Raid on Gang Leader's Headquarters (November 27, 2024):
   Location: Baz Delmas neighborhood, Port-au-Prince.
   Perpetrators: Multinational Security Support Mission (MSSM) and Haitian National Police (HNP).
   Target: Jimmy "Barbecue" Chérizier, leader of the G9 gang coalition.
   Details: A dawn raid utilizing an armored bulldozer targeted Chérizier's fortified headquarters. Despite breaching 
   the stronghold and destroying his residence, Chérizier and his militia managed to escape, leaving behind weapons 
   and vehicles.

Key Actors:

- Jimmy "Barbecue" Chérizier: A former police officer turned gang leader, Chérizier heads the "Revolutionary Forces 
  of the G9 Family and Allies," a coalition controlling over 80% of Port-au-Prince. His group is implicated in numerous 
  violent acts, including massacres and kidnappings.

- Gran Grif Gang: Operating in the Artibonite Department, this gang is responsible for the Pont-Sondé massacre and is 
  considered one of Haiti's most brutal criminal organizations.

Impact on Civilians:

- Displacement: Over 700,000 Haitians are internally displaced due to gang violence, with more than half being children.

- Casualties: In the past week alone, over 150 people have been killed in Port-au-Prince as gangs seized control of 
  most of the capital.

- Child Recruitment: There has been a 70% increase in the recruitment of children by gangs over the past year, with 
  minors being used as informers, armed participants, and subjected to exploitation.

International Response:

- Multinational Security Support Mission (MSSM): Comprising contingents from Kenya, Jamaica, and Belize, the MSSM 
  was deployed to assist the Haitian National Police. However, challenges such as underfunding and inadequate staffing 
  have hindered its effectiveness.

- United Nations: The UN has initiated staff evacuations and is urging stronger global support to address the escalating 
  violence. Efforts to transform the support mission into a full peacekeeping operation have faced resistance.

Conclusion:

Haiti's security situation continues to deteriorate, with armed gangs exerting significant control over the capital and 
other regions. The violence has led to mass casualties, widespread displacement, and a deepening humanitarian crisis. 
Despite international efforts, including the deployment of multinational forces, the challenges remain substantial, 
necessitating urgent and coordinated action to restore stability and protect civilians.
"""
new_report_title = "Haiti Situation Report - New Report"
new_report_url = "https://example.com/new_report"

# Process the new report
new_report = classify_new_report(new_report_text, new_report_title, new_report_url)

# Step 7: Save the new report to a new CSV file
new_output_csv = "new_haiti_situation_report_classified.csv"

# Check if the file exists to either create or append
import os

if os.path.exists(new_output_csv):
    # Append to the existing file
    existing_df = pd.read_csv(new_output_csv)
    updated_df = pd.concat([existing_df, pd.DataFrame([new_report])], ignore_index=True)
else:
    # Create a new file
    updated_df = pd.DataFrame([new_report])

# Save the updated data
updated_df.to_csv(new_output_csv, index=False)
print(f"New report classified and saved to {new_output_csv}")
