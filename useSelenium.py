import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Set up the webdriver with webdriver-manager to handle ChromeDriver installation
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()

# Initialize the Chrome driver with the correct service and options
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the website
driver.get("https://njdg.ecourts.gov.in/scnjdg/")

# Wait for the page to load
time.sleep(5)

# List of different CSS selectors to extract data
selectors = [
    ".card-header.pe-1",  # Example selector
    ".card.mb-2.aos-init.aos-animate",  # Add more selectors as needed
    ".card.aos-init.aos-animate",
    ".col-md.aos-init.aos-animate",
    ".col-md p",
]

# Create a list to store the data
data = []

# Initialize a card index
card_index = 1

# Loop through each selector
for selector in selectors:
    # Find all elements for the current selector
    cards = driver.find_elements(By.CSS_SELECTOR, selector)

    # Loop through each card and extract the text
    for card in cards:
        text = card.text

        # Clean up the text by removing excessive whitespaces and newlines
        cleaned_text = re.sub(r'\s*\n\s*', ' ', text).strip()

        # Store the text in a structured format
        card_data = {
            "card_number": card_index,
            "selector": selector,
            "content": cleaned_text
        }

        data.append(card_data)

        # Increment the card index
        card_index += 1

# Extract links from the footer
footer_links_selector = ".col.footerlinks li a"  # Update this if the structure changes
footer_links = driver.find_elements(By.CSS_SELECTOR, footer_links_selector)

# Create a list to store footer links
footer_links_data = []

for link in footer_links:
    link_text = link.text.strip()
    link_href = link.get_attribute("href")
    footer_links_data.append({"text": link_text, "url": link_href})

# Add footer links to data
data.append({
    "footer_links": footer_links_data
})

# Close the webdriver
driver.quit()

# Save the data to a JSON file with key-value pairs
with open("myscrappeddata.json", "w") as file:
    json.dump(data, file, indent=4)

print("Scraping completed and data saved to 'myscrappeddata.json'.")
