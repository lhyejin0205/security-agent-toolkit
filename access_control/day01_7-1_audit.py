from rbac import check_permission, ROLES, USERS
from access_log import LOG

allowed = 0
denied = 0
counts = {}
used = {}

for log_id, time, user, resource, action in LOG:
    ok, reason = check_permission(user, resource, action)
    if ok:
        allowed += 1
        counts[user + " 허용"] = counts.get(user + " 허용", 0) + 1
        role = USERS[user]["role"]
        if role not in used:
            used[role] = []
        used[role].append(resource + ":" + action)
    else:
        denied += 1
        print("[거부]", log_id, time, user, resource, action, "-", reason)
        counts[user + " 거부"] = counts.get(user + " 거부", 0) + 1

print("허용", allowed, "거부", denied)
print(counts)

for role, permissions in ROLES.items():
    for permission in permissions:
        if permission not in used.get(role, []):
            print("쓰이지 않음", role, permission)
