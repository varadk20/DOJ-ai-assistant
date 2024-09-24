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
    ".col-md-3.aos-init.aos-animate",  # Example selector
    ".col-md-3",                    # Add more selectors as needed
    ".col-md.aos-init.aos-animate",
    ".col-md"
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

# Close the webdriver
driver.quit()

# Save the data to a JSON file with key-value pairs
with open("myscrappeddata.json", "w") as file:
    json.dump(data, file, indent=4)

print("Scraping completed and data saved to 'myscrappeddata.json'.")
