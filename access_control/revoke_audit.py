def decide_reason(plan, users):
    reasons = plan.get("reasons", [])
    if reasons:
        return ", ".join(reasons)
    if "예외" in plan["source"]:
        return "예외 회수 (사유 키 없음)"
    if not users[plan["user"]]["employed"]:
        return "퇴사자 역할 권한 회수 (사유 키 없음)"
    return "역할 권한 회수 (사유 키 없음)"


def decide_approver(plan, decisions):
    if plan["approval"] == "승인됨":
        return "보안 책임자"
    if plan["approval"] == "승인 불필요":
        return "해당 없음(규칙상 승인 대상 아님)"
    return "미정(승인 대기)"


def add_audit_keys(log, plans, users, decisions, before, after, executor):
    audited = []
    for i in range(len(log)):
        entry = log[i].copy()
        plan = plans[i]
        entry["reason"] = decide_reason(plan, users)
        entry["approver"] = decide_approver(plan, decisions)
        if entry["result"] == "실행":
            entry["executor"] = executor
        else:
            entry["executor"] = "미실행"
        entry["target"] = plan["target"]
        entry["before"] = before[i]
        entry["after"] = after[i]
        audited.append(entry)
    return audited
