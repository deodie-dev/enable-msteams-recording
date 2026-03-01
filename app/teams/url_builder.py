def build_meeting_options_url(user_id: str, tenant_id: str, meeting_id: str):
    return (
        f"https://teams.microsoft.com/meetingOptions/"
        f"?organizerId={user_id}"
        f"&tenantId={tenant_id}"
        f"&threadId=19_{meeting_id}"
        f"&messageId=0"
        f"&language=en-US"
    )