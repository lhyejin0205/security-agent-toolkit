import json
from datetime import datetime
from pathlib import Path

EXCEPTIONS_PATH = Path(__file__).resolve().parent / "config" / "exceptions.json"
with EXCEPTIONS_PATH.open(encoding="utf-8") as f:
    EXCEPTIONS = json.load(f)

TIME_FORMAT = "%Y-%m-%d %H:%M"


def find_exception(user, permission, now):
    """Return (True, exception id) if a matching exception is active, else (False, None)."""
    for exc in EXCEPTIONS:
        if exc["user"] == user and exc["permission"] == permission:
            expires = datetime.strptime(exc["expires"], TIME_FORMAT)
            if now < expires:
                return True, exc["id"]
    return False, None
