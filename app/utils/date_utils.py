from datetime import datetime, timedelta
import pytz


def get_date_range(days: int):
    utc_now = datetime.now(pytz.utc)
    end_date_utc = utc_now + timedelta(days=days)

    start_date = utc_now.strftime('%Y-%m-%dT00:00:00Z')
    end_date = end_date_utc.strftime('%Y-%m-%dT23:59:59Z')

    return start_date, end_date