from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import requests
from datetime import datetime, timedelta
import pytz
import urllib.parse
import re
import sys

from dotenv import load_dotenv
import os
load_dotenv()

if len(sys.argv) != 3:
    print("Usage: python auto_record.py <EMAIL> <PASSWORD>")
    sys.exit(1)

EMAIL = sys.argv[1]
PASSWORD = sys.argv[2]

# BA_LIST = os.environ.get("BA_LIST")
GRAPH_API_URL = os.environ.get("GRAPH_API_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
TENANT_ID = os.environ.get("TENANT_ID")
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")

def get_user_id_by_email(email, access_token, get_value):

    url = f"https://graph.microsoft.com/v1.0/users?$filter=mail eq '{email}'"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        users = data.get("value", [])
        if users:
            return users[0].get(get_value)
        else:
            print("No user found with that email.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
# user_ID = None
# for ba in BA_LIST:
#     if ba["email"].lower() == EMAIL.lower():
#         user_ID = ba["mID"]
#         break  

# print(f"User ID: {user_ID}")

# Get Global Access Token for Graph API
def get_global_graphAPI_token():
    
    url = GRAPH_API_URL
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

# Parse the event details
def parse_event(event):
    event_details = {
        "event_id": event.get("id"),
        "online_meeting": event.get("onlineMeeting"),
        "joinURL": event.get("onlineMeeting").get("joinUrl", "None") if event.get("onlineMeeting") else "None",
        "is_online_meeting": event.get("isOnlineMeeting"),
        "subject": event.get("subject", "No Subject"),
        "organizer": event.get("organizer", {}).get("emailAddress", {}).get("name", "Unknown Organizer"),
        "start_time": event.get("start", {}).get("dateTime", "No Start Time"),
        "trimmed_st": event.get("start", {}).get("dateTime", "No Start Time")[:23],
        "formatted_st": event.get("start", {}).get("dateTime", "No Start Time")[:23].replace("T", " "),
        "end_time": event.get("end", {}).get("dateTime", "No End Time"),
        "trimmed_et": event.get("end", {}).get("dateTime", "No End Time")[:23],
        "formatted_et": event.get("end", {}).get("dateTime", "No End Time")[:23].replace("T", " "),
        "categories_str": ', '.join(event.get("categories", [])) if event.get("categories", []) else 'No Categories',}
    
    return event_details

utc_now = datetime.now(pytz.utc) 
start_date = utc_now.strftime('%Y-%m-%dT00:00:00Z')
end_date_utc = utc_now + timedelta(days=7)
end_date = end_date_utc.strftime('%Y-%m-%dT23:59:59Z')

# Fetch calendar events from Outlook
def get_outlook_metadata(access_token, user, start_date, end_date):

    calendar_events = []
    events = []

    url = f"https://graph.microsoft.com/v1.0/users/{user}/calendarview?$top=1000&$count=true&startDateTime={start_date}&endDateTime={end_date}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Prefer": 'outlook.timezone="Asia/Singapore"',
        "Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        events = data.get("value", [])
        for event in events:
            calendar_events.append(parse_event(event))
    else:
        print(f"Error {response.status_code}: {response.text}")

    return calendar_events

access_token = get_global_graphAPI_token ()

calendar_events = get_outlook_metadata(access_token, EMAIL, start_date, end_date)

# Extract meeting ID from join URL
def extract_meeting_id_from_join_url(join_url):
    decoded_url = urllib.parse.unquote(join_url)
    match = re.search(r'\d+:meeting_[\w-]+@[\w.-]+', decoded_url)
    return match.group(0) if match else None

# Prepare URLs for processing. Loop through events and filter based on categories
URLS = []
print(f"\nWill process the following calendar events:")
for event in calendar_events:
    if not ('client - retainer' in event.get("categories_str").lower() or 'client - diagnostic' in event.get("categories_str").lower()):
        continue

    id_from_url = extract_meeting_id_from_join_url(event.get("joinURL"))[3:]
    meeting_options_url = f"https://teams.microsoft.com/meetingOptions/?organizerId={user_ID}&tenantId={TENANT_ID}&threadId=19_{id_from_url}&messageId=0&language=en-US"
    print(f"Date & Time: {event.get("formatted_st", "")} | Subject: {event.get("subject", "No Subject")} | URL: {meeting_options_url}")
    URLS.append(meeting_options_url)


# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
driver.get("https://login.microsoftonline.com")

# Login
try:
    wait = WebDriverWait(driver, 20)

    # Enter Email
    email_input = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
    email_input.send_keys(EMAIL)
    next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    next_button.click()
    
    time.sleep(2)

    # Enter Password
    password_input = wait.until(EC.presence_of_element_located((By.ID, "i0118")))
    password_input.send_keys(PASSWORD)
    signin_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    signin_button.click()
    time.sleep(2)

    # (Optional) "Stay signed in?" — handle if it appears
    try:
        stay_signed_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
        stay_signed_in_button.click()
        time.sleep(2)
    except:
        pass

    print("\nSuccessfully signed in.")

except Exception as e:
    print(f"Login failed: {e}")

time.sleep(5)

# Process each URL to enable auto-recording
for url in URLS:
    print(f"\nProcessing URL: {url}")
    driver.get(url)

    try:
        checkbox_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "AutoRecordingEnabled")))

        # Check current state of the checkbox. If not checked, click to enable
        label = checkbox_input.find_element(By.XPATH, "./..")
        is_checked = checkbox_input.get_attribute("aria-checked")
        print(f"Checkbox currently checked: {is_checked}")

        if is_checked == "false":
            label.click()
            print("Checkbox was OFF. Now turned ON.")
            save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Save"]')))
            save_button.click()
            print("Clicked the Save button.")
            time.sleep(2)
            
        else:
            print("Checkbox already ON.")
            time.sleep(1)

    except Exception as e:
        print(f"Error processing {url}: {e}")

driver.quit()