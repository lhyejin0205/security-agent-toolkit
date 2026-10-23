from rbac import check_permission
from exception_policy import EXCEPTIONS


def grant_request(request):
    """승인된 요청서를 정책으로 한 번 더 확인하고, 통과하면 예외 권한을 부여한다. (성공 여부, 이유)를 리턴한다."""
    if request["status"] != "approved":
        return False, "승인되지 않음"

    ok, judge_reason = check_permission(
        request["user"], request["resource"], request["action"]
    )
    if ok or judge_reason != "권한 없음":
        return False, f"부여하지 않음({judge_reason})"

    exception = {
        "id": len(EXCEPTIONS) + 1,
        "user": request["user"],
        "permission": request["permission"],
        "expires": request["until"],
        "reason": request["reason"],
    }
    EXCEPTIONS.append(exception)
    request["exception_id"] = exception["id"]
    request["status"] = "granted"
    return True, "부여"
