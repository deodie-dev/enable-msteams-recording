import urllib.parse
import re


def extract_meeting_id_from_join_url(join_url: str):
    if not join_url:
        return None

    decoded_url = urllib.parse.unquote(join_url)
    match = re.search(r'\d+:meeting_[\w-]+@[\w.-]+', decoded_url)

    return match.group(0) if match else None