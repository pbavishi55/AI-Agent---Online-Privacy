import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# List of known data broker opt-out URLs
DATA_BROKER_URLS = [
    "https://www.whitepages.com/suppression_requests",
    "https://www.spokeo.com/optout",
    "https://www.mylife.com/ccpa",
    "https://www.truepeoplesearch.com/removal",
    # Add more data brokers here
]

PHONE_NUMBER = "612-433-2136"  # Replace with your number
EMAIL = "pankaj.bavishi@gmail.com"  # Required for some requests

# Function to check if phone number exists on a broker's site
def search_phone_number(url, phone):
    search_url = f"{url}/search?q={phone}"
    response = requests.get(search_url)
    if response.status_code == 200 and phone in response.text:
        return True
    return False

# Function to automate opt-out request submission
def submit_opt_out(url):
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
    driver.get(url)
    time.sleep(2)

    try:
        # Locate and fill form elements (This depends on the website's structure)
        phone_input = driver.find_element(By.NAME, "phone")
        phone_input.send_keys(PHONE_NUMBER)
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.RETURN)

        time.sleep(3)  # Allow submission processing
        print(f"Opt-out request submitted for {url}")
    except Exception as e:
        print(f"Failed on {url}: {e}")
    finally:
        driver.quit()

# Main function to run the AI agent
def ai_agent_remove_phone():
    for broker in DATA_BROKER_URLS:
        print(f"Checking {broker} for phone number...")
        if search_phone_number(broker, PHONE_NUMBER):
            print(f"Phone number found on {broker}. Submitting removal request...")
            submit_opt_out(broker)
        else:
            print(f"No phone number found on {broker}. Skipping...")

# Run the AI agent
ai_agent_remove_phone()
