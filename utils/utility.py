from datetime import timezone, timedelta


IST = timezone(timedelta(hours=5, minutes=30))  # Define IST timezone once

def format_datetime_to_ist(dt):
    """Convert a datetime object to IST timezone and format it as a string."""
    return dt.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S")
