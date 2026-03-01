def parse_event(event: dict) -> dict:
    start = event.get("start", {}).get("dateTime", "")
    end = event.get("end", {}).get("dateTime", "")

    return {
        "event_id": event.get("id"),
        "joinURL": event.get("onlineMeeting", {}).get("joinUrl"),
        "subject": event.get("subject", "No Subject"),
        "organizer": event.get("organizer", {})
            .get("emailAddress", {})
            .get("name", "Unknown Organizer"),
        "start_time": start,
        "end_time": end,
        "categories_str": ", ".join(event.get("categories", [])) or "No Categories",
    }


def get_user_id_by_email(client, email: str):
    params = {"$filter": f"mail eq '{email}'"}
    data = client.get("users", params=params)
    users = data.get("value", [])

    if not users:
        raise Exception("User not found")

    return users[0].get("id")


def get_outlook_metadata(client, user: str, start_date: str, end_date: str):
    params = {
        "$top": 1000,
        "startDateTime": start_date,
        "endDateTime": end_date
    }

    data = client.get(f"users/{user}/calendarview", params=params)
    events = data.get("value", [])

    return [parse_event(event) for event in events]