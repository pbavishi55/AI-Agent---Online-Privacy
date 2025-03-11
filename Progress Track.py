import time
import sqlite3
import requests
import pandas as pd
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# List of known people search sites
PEOPLE_SEARCH_SITES = {
    "Spokeo": "https://www.spokeo.com/optout",
    "WhitePages": "https://www.whitepages.com/suppression_requests",
    "TruePeopleSearch": "https://www.truepeoplesearch.com/removal",
    "MyLife": "https://www.mylife.com/ccpa",
}

# User details
FULL_NAME = "Jigar Doshi"
PHONE_NUMBER = "612-433-2136"
EMAIL = "pnkaj.bavishi@gmail.com"
ADDRESS = "1104 Laurtrec Terrace, Sunnyvale, CA 94087"

# Database connection
conn = sqlite3.connect("removal_progress.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS removals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT,
        status TEXT,
        last_attempt TEXT
    )
""")
conn.commit()

# Function to log removal status
def log_status(site, status):
    cursor.execute("INSERT INTO removals (site, status, last_attempt) VALUES (?, ?, datetime('now'))", 
                   (site, status))
    conn.commit()

# Function to submit opt-out request
def submit_opt_out(site, url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(20)

    try:
        if "spokeo" in url:
            driver.find_element(By.NAME, "phone").send_keys(PHONE_NUMBER)
            driver.find_element(By.NAME, "email").send_keys(EMAIL)
           
            
        elif "whitepages" in url:
            driver.find_element(By.NAME, "name").send_keys(FULL_NAME)
           
        elif "truepeoplesearch" in url:
            driver.find_element(By.NAME, "address").send_keys(ADDRESS)
       

        driver.find_element(By.NAME, "submit").click()
        time.sleep(3)

        log_status(site, "Submitted")
        print(f"Opt-out request submitted for {site}")

    except Exception as e:
        log_status(site, f"Failed: {e}")
        print(f"Failed on {site}: {e}")
    finally:
        driver.quit()

# Function to generate and send progress report
def send_progress_report():
    df = pd.read_sql("SELECT * FROM removals", conn)
    report_content = df.to_html(index=False)

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = "AI Agent: Removal Progress Report"

    msg.attach(MIMEText(report_content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, "your-email-password")
        server.sendmail(EMAIL, EMAIL, msg.as_string())

    print("Progress report emailed!")

# Function to run the AI agent
def ai_agent_remove_personal_info():
    for site, url in PEOPLE_SEARCH_SITES.items():
        print(f"Processing {site}...")
        submit_opt_out(site, url)

# Run the AI agent
ai_agent_remove_personal_info()
send_progress_report()