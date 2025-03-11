import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# List of known people search sites
PEOPLE_SEARCH_SITES = [
    "https://www.spokeo.com/optout",
    "https://www.whitepages.com/suppression_requests",
    "https://www.truepeoplesearch.com/removal",
    "https://www.mylife.com/ccpa",
    "https://www.beenverified.com/app/optout/search",
]

FULL_NAME = "John Doe"  # Replace with your name
PHONE_NUMBER = "123-456-7890"  # Replace with your phone number
EMAIL = "your-email@example.com"  # Used for verification
ADDRESS = "123 Main St, City, State, ZIP"  # If required

# Function to search for personal info on a site
def search_personal_info(url, name):
    search_url = f"{url}/search?q={name.replace(' ', '+')}"
    response = requests.get(search_url)
    
    if response.status_code == 200 and name.lower() in response.text.lower():
        return True
    return False

# Function to submit an opt-out request
def submit_opt_out(url):
    driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
    driver.get(url)
    time.sleep(2)

    try:
        if "spokeo" in url:  # Example for Spokeo
            search_box = driver.find_element(By.NAME, "phone")
            search_box.send_keys(PHONE_NUMBER)
            email_input = driver.find_element(By.NAME, "email")
            email_input.send_keys(EMAIL)
            email_input.send_keys(Keys.RETURN)
        elif "whitepages" in url:  # Example for WhitePages
            search_box = driver.find_element(By.NAME, "name")
            search_box.send_keys(FULL_NAME)
            search_box.send_keys(Keys.RETURN)
        elif "truepeoplesearch" in url:  # Example for TruePeopleSearch
            search_box = driver.find_element(By.NAME, "address")
            search_box.send_keys(ADDRESS)
            search_box.send_keys(Keys.RETURN)

        time.sleep(3)
        print(f"Opt-out request submitted for {url}")
    except Exception as e:
        print(f"Failed on {url}: {e}")
    finally:
        driver.quit()

# Function to automate the removal process
def ai_agent_remove_personal_info():
    for site in PEOPLE_SEARCH_SITES:
        print(f"Checking {site} for personal info...")
        if search_personal_info(site, FULL_NAME):
            print(f"Personal info found on {site}. Submitting removal request...")
            submit_opt_out(site)
        else:
            print(f"No personal info found on {site}. Skipping...")

# Run the AI agent
ai_agent_remove_personal_info()
