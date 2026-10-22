from exception_policy import find_exception
from rbac import check_permission


def evaluate_access(user, resource, action, now):
    """Return a final access decision after role and temporary-exception checks."""
    ok, reason = check_permission(user, resource, action)
    if ok:
        return True, "역할 권한"
    if reason != "권한 없음":
        return False, reason

    found, exc_id = find_exception(user, f"{resource}:{action}", now)
    if found:
        return True, f"예외 {exc_id}번"
    return False, "권한 없음"
