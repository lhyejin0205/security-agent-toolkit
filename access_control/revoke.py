import json


def remove_exception(exceptions, target_id):
    for exc in exceptions:
        if exc["id"] == target_id:
            exceptions.remove(exc)
            return True
    return False


def apply_plan(plan, users, roles, exceptions):
    if plan["method"] == "예외 삭제":
        remove_exception(exceptions, plan["target"])
    elif plan["method"] == "역할 해제":
        user_info = users[plan["target"]]
        user_info["role"] = ""
    else:
        role_permissions = roles[plan["target"]]
        role_permissions.remove(plan["permission"])


def save_log(log, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    return len(log)


def execute_revocation(plans, users, roles, exceptions, now):
    log = []
    for plan in plans:
        if plan["approval"] == "승인 대기":
            result = "대기"
        else:
            apply_plan(plan, users, roles, exceptions)
            result = "실행"
        entry = {
            "time": now,
            "user": plan["user"],
            "permission": plan["permission"],
            "method": plan["method"],
            "approval": plan["approval"],
            "result": result,
        }
        log.append(entry)
    return log
