from datetime import datetime, date
from typing import Optional


def parse_dates(dates: Optional[dict]) -> Optional[dict]:
    """
    Parse dates from string to date object
    :param dates: dict
    :return: Optional[dict]
    """
    if not dates:
        return None
    try:
        return {key: datetime.strptime(val, "%Y-%m-%d").date() for key, val in dates.items()}
    except KeyError as e:
        raise KeyError(f"Date key error: {e}")
    except ValueError as e:
        raise ValueError(f"Date format error: {e}")


def parse_date(date_string: Optional[str]) -> Optional[date]:
    """
    Parse date from string to date object.
    :param date_string: str
    :return: Optional[datetime]
    """
    if not date_string:
        return None

    try:
        # Strip the time portion if it exists (remove everything after the 'T')
        date_string = date_string.split("T")[0]
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Date format error: {e}")
