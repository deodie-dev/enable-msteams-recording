import sys
from app.settings import (NO_OF_DAYS, TENANT_ID, RESTRICTED_USERS)
from app.utils.date_utils import get_date_range
from app.graph.auth import get_global_graph_token
from app.graph.client import GraphClient
from app.graph.calendar_service import get_user_id_by_email, get_outlook_metadata
from app.teams.url_builder import build_meeting_options_url
from app.teams.recording_services import enable_auto_recording
from app.automation.selenium_driver import create_driver
from app.automation.login import login_microsoft
from app.utils.meeting_utils import extract_meeting_id_from_join_url


# def is_restricted(event):
#     subject = event.get("subject", "").lower()
#     organizer = event.get("organizer", "").lower()

#     for rule in RESTRICTED_USERS:
#         if (rule["subject"].lower() in subject or rule["email"].lower() in organizer):
#             return True
#     return False
def is_restricted(event: dict) -> bool:
    subject = event.get("subject", "").lower()
    recipients = event.get("recipients", [])

    for rule in RESTRICTED_USERS:
        subject_match = rule["subject"].lower() in subject
        recipient_match = any(
            rule["email"].lower() == recipient
            for recipient in recipients
        )

        if subject_match or recipient_match:
            return True

    return False

def main():
    
    if len(sys.argv) != 3:
        print("Usage: python main.py <email> <password>")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]

    start_date, end_date = get_date_range(NO_OF_DAYS)

    token = get_global_graph_token()
    client = GraphClient(token)

    user_id = get_user_id_by_email(client, email)
    events = get_outlook_metadata(client, email, start_date, end_date)

    urls = []
    urls_restricted = []

    for event in events:

        categories = event.get("categories_str", "").lower()
        if not ("client - retainer" in categories or "client - diagnostic" in categories):
            continue

        meeting_id_raw = extract_meeting_id_from_join_url(event.get("joinURL"))
        if not meeting_id_raw:
            continue

        meeting_id = meeting_id_raw[3:]
        url = build_meeting_options_url(user_id, TENANT_ID, meeting_id)
        if is_restricted(event):
            urls_restricted.append(url)
        else:
            urls.append(url)

    driver = create_driver()

    try:
        login_microsoft(driver, email, password)

        for url in urls:
            enable_auto_recording(driver, url, True)

        for url in urls_restricted:
            enable_auto_recording(driver, url, False)

    finally:
        driver.quit()
        

if __name__ == "__main__":
    main()