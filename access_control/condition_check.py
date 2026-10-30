from policy import evaluate_access

WORK_START = 9
WORK_END = 18


def check_conditions(hour, location):
    reasons = []
    if hour < WORK_START or hour >= WORK_END:
        reasons.append("업무 시간 밖")
    if location != "내부":
        reasons.append("외부 접속")
    return reasons


def decide_request(request, now):
    resource, action = request["permission"].split(":")
    ok, reason = evaluate_access(request["user"], resource, action, now)
    if not ok:
        return False, [reason]
    reasons = check_conditions(request["hour"], request["location"])
    if reasons:
        return False, reasons
    return True, ["허용"]
