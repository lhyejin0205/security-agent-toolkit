def approve_request(request, approver):
    """검토 중(reviewing)인 요청서만 승인한다. (성공 여부, 이유)를 리턴한다."""
    if request["status"] != "reviewing":
        return False, "검토 중이 아님"
    if request["user"] == approver:
        return False, "본인 요청은 처리할 수 없음"
    request["status"] = "approved"
    request["approver"] = approver
    return True, "승인"


def reject_request(request, approver):
    """검토 중(reviewing)인 요청서만 반려한다. (성공 여부, 이유)를 리턴한다."""
    if request["status"] != "reviewing":
        return False, "검토 중이 아님"
    if request["user"] == approver:
        return False, "본인 요청은 처리할 수 없음"
    request["status"] = "rejected"
    request["approver"] = approver
    return True, "반려"
