from rbac import USERS

REQUESTS = []


def create_request(user, resource, action, until, reason, received_at):
    """요청서를 만들어 REQUESTS 에 넣고 (True, 요청서)를 리턴한다. 접수할 수 없으면 (False, 이유)를 리턴한다."""
    if user not in USERS:
        return False, "등록되지 않은 사용자"
    if reason == "":
        return False, "이유가 없음"
    if until <= received_at:
        return False, "만료 시각이 이미 지났음"

    request = {
        "id": len(REQUESTS) + 1,
        "user": user,
        "resource": resource,
        "action": action,
        "permission": f"{resource}:{action}",
        "until": until,
        "reason": reason,
        "requested_at": received_at,
        "status": "reviewing",
    }
    REQUESTS.append(request)
    return True, request
