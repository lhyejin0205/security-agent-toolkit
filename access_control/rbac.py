import json

with open("config/roles.json", encoding="utf-8") as f:
    ROLES = json.load(f)
with open("config/users.json", encoding="utf-8") as f:
    USERS = json.load(f)


def check_permission(user, resource, action):
    """Return whether the user may perform the requested action, and why."""
    if user not in USERS:
        return False, "등록되지 않은 사용자"
    if not USERS[user]["employed"]:
        return False, "퇴사한 계정"

    role = USERS[user]["role"]
    if role not in ROLES:
        return False, "역할이 없음"

    permission = f"{resource}:{action}"
    if permission not in ROLES[role]:
        return False, "권한 없음"

    return True, "허용"
