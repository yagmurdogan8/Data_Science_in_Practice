import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Main page URL containing links to reports
main_url = "https://www.eepa.be/?page_id=8014"

# Step 2: Function to fetch links from the main page
def fetch_report_links(main_url):
    response = requests.get(main_url)
    if response.status_code != 200:
        print(f"Failed to fetch main page, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    report_links = []

    # Extract links with titles containing "Haiti Situation Report"
    for link in soup.find_all("a"):
        title = link.get_text(strip=True)
        href = link.get("href")
        if "Haiti Situation Report" in title and href:
            report_links.append({"title": title, "url": href})

    return report_links

# Step 3: Function to fetch content between "Situation in Haiti" and "Links of interest"
def fetch_targeted_content(url, start_phrase="Situation in Haiti", end_phrase="Links of interest"):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to fetch page, status code: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the full article text
        article = soup.find("article")
        if article:
            full_text = article.get_text(strip=True, separator="\n")

            # Locate the start and end phrases
            start_idx = full_text.find(start_phrase)
            end_idx = full_text.find(end_phrase)

            if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                # Extract content between the phrases
                return full_text[start_idx + len(start_phrase):end_idx].strip()
            else:
                return f"Section between '{start_phrase}' and '{end_phrase}' not found."
        else:
            return "Article content not found."
    except Exception as e:
        return f"Error occurred: {e}"

# Step 4: Main logic to process all links
def process_reports(main_url, output_csv="haiti_situation_reports_final.csv"):
    # Fetch links from the main page
    report_links = fetch_report_links(main_url)

    # Initialize a list to store the extracted data
    extracted_data = []

    # Fetch content for each report
    for report in report_links:
        print(f"Processing: {report['title']} - {report['url']}")
        content = fetch_targeted_content(report['url'])
        extracted_data.append({
            "title": report["title"],
            "url": report["url"],
            "content": content
        })

    # Export data to a CSV file
    df = pd.DataFrame(extracted_data)
    df.to_csv(output_csv, index=False)
    print(f"Reports saved to {output_csv}")

# Step 5: Run the script
process_reports(main_url)
