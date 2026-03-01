import sys
from app.settings import (GRAPH_API_URL, NO_OF_DAYS, CLIENT_ID, CLIENT_SECRET, TENANT_ID, CHROMEDRIVER_PATH, RESTRICTED_USERS)
# from app.utils.date_utils import get_date_range
# from app.graph.auth import get_global_graph_token
# from app.graph.client import GraphClient
# from app.graph.calendar_service import get_user_id_by_email, get_outlook_metadata
# from app.teams.url_builder import build_meeting_options_url
# # from app.teams.recording_service import enable_auto_recording
# from app.automation.selenium_driver import create_driver
# from app.automation.login import login_microsoft
# from app.utils.meeting_utils import extract_meeting_id_from_join_url


def is_restricted(event):
    subject = event.get("subject", "").lower()
    organizer = event.get("organizer", "").lower()

    for rule in RESTRICTED_USERS:
        if (
            rule["subject"].lower() in subject
            or rule["email"].lower() in organizer
        ):
            return True
    return False


def main():
    event = {
        "subject": "Restricted Meeting - Strategy Call",
        "organizer": "ceo@companyemail.co"
    }

    if is_restricted(event):
        print(f"Success")
        



if __name__ == "__main__":
    main()