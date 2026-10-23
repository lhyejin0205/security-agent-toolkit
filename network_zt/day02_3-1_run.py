import json
from datetime import datetime
from pathlib import Path

from exception_policy import EXCEPTIONS, TIME_FORMAT, find_exception

LESSON_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LESSON_DIR.parent
USERS_PATH = PROJECT_DIR / "access_control" / "config" / "users.json"
NOW = datetime.strptime("2026-10-22 14:00", TIME_FORMAT)

CHECKS = [
    ("seoyeon", "SETTLE:QUERY"),
    ("junho", "SALES:CHANGE"),
    ("dami", "SALES:QUERY"),
    ("batch-night", "SALES:QUERY"),
    ("gaeun", "SETTLE:QUERY"),
    ("seoyeon", "ACCOUNT:CHANGE"),
]

print("--- 단계 1: 판정 - 지금 유효한 예외가 있나")
for user, permission in CHECKS:
    print(user, permission, "->", find_exception(user, permission, NOW))

with USERS_PATH.open(encoding="utf-8") as f:
    USERS = json.load(f)

print("--- 단계 2: 점검 - 예외 목록에서 회수할 것")
for exc in EXCEPTIONS:
    expires = datetime.strptime(exc["expires"], TIME_FORMAT)
    if NOW >= expires:
        print("[회수] 만료됨", exc["id"], exc["user"], exc["permission"], exc["expires"])
    elif not USERS[exc["user"]]["employed"]:
        print("[회수] 퇴사자", exc["id"], exc["user"], exc["permission"], exc["expires"])
    else:
        print("[유지]", exc["id"], exc["user"], exc["permission"], exc["expires"])
