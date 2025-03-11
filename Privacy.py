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

# List of data brokers (this list can be dynamically updated)
PEOPLE_SEARCH_SITES = {
    "Spokeo": "https://www.spokeo.com/optout",
    "WhitePages": "https://www.whitepages.com/suppression_requests",
    "TruePeopleSearch": "https://www.truepeoplesearch.com/removal",
    "BeenVerified": "https://www.beenverified.com/app/optout/search",
    "MyLife": "https://www.mylife.com/ccpa",
    "Intelius": "https://www.intelius.com/opt-out",
    "FastPeopleSearch": "https://www.fastpeoplesearch.com/removal",
}

# Personal data (can be expanded with past info)
PERSONAL_INFO = {
    "names": ["Pankaj Bavishi"],
    "emails": ["pankaj.bavishi@gmail.com", "pbavishi@ehotmail.com"],
    "phone_numbers": ["612-433-2136", "+919970015723"],
    "addresses": ["123 Main St, City, State, ZIP", "Previous Address, State"],
}

# Database setup
conn = sqlite3.connect("privacy_tracking.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS removals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT,
        personal_info TEXT,
        status TEXT,
        last_attempt TEXT
    )
""")
conn.commit()

# Function to log removal status
def log_status(site, personal_info, status):
    cursor.execute("INSERT INTO removals (site, personal_info, status, last_attempt) VALUES (?, ?, ?, datetime('now'))", 
                   (site, str(personal_info), status))
    conn.commit()

# Function to submit opt-out request
def submit_opt_out(site, url, personal_info):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    try:
        if "spokeo" in url:
            driver.find_element(By.NAME, "phone").send_keys(personal_info["phone_numbers"][0])
            driver.find_element(By.NAME, "email").send_keys(personal_info["emails"][0])
        elif "whitepages" in url:
            driver.find_element(By.NAME, "name").send_keys(personal_info["names"][0])
        elif "truepeoplesearch" in url:
            driver.find_element(By.NAME, "address").send_keys(personal_info["addresses"][0])

        driver.find_element(By.NAME, "submit").click()
        time.sleep(3)

        log_status(site, personal_info, "Submitted")
        print(f"Opt-out request submitted for {site}")

    except Exception as e:
        log_status(site, personal_info, f"Failed: {e}")
        print(f"Failed on {site}: {e}")
    finally:
        driver.quit()

# Function to generate and send progress report
def send_progress_report():
    df = pd.read_sql("SELECT * FROM removals", conn)
    report_content = df.to_html(index=False)

    msg = MIMEMultipart()
    msg["From"] = PERSONAL_INFO["emails"][0]
    msg["To"] = PERSONAL_INFO["emails"][0]
    msg["Subject"] = "AI Agent: Privacy Removal Progress Report"

    msg.attach(MIMEText(report_content, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(PERSONAL_INFO["emails"][0], "your-email-password")
        server.sendmail(PERSONAL_INFO["emails"][0], PERSONAL_INFO["emails"][0], msg.as_string())

    print("Privacy report emailed!")

# Function to run the AI agent
def ai_agent_remove_personal_info():
    for site, url in PEOPLE_SEARCH_SITES.items():
        print(f"Processing {site}...")
        submit_opt_out(site, url, PERSONAL_INFO)

# Run the AI agent
ai_agent_remove_personal_info()
send_progress_report()
