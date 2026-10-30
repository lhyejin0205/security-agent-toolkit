from datetime import datetime
from rbac import USERS, ROLES
from exception_policy import EXCEPTIONS, TIME_FORMAT
from policy import evaluate_access
from config_loader import load_json
from revoke_input import load_to_revoke
from revoke_plan import plan_revocation
from revoke_approve import load_sensitive, mark_approvals
from revoke import execute_revocation, save_log
from revoke_audit import add_audit_keys

NOW_TEXT = "2026-10-30 10:00"
NOW = datetime.strptime(NOW_TEXT, TIME_FORMAT)
DECISIONS = {"dami:SALES:QUERY": "승인", "dami:SALES:CHANGE": "승인"}
EXECUTOR = "임혜진"

to_revoke = load_to_revoke()
plans = plan_revocation(to_revoke, USERS, ROLES)
sensitive = load_sensitive("config/sensitive.json")
plans = mark_approvals(plans, sensitive, DECISIONS)


def judge(plan):
    resource, action = plan["permission"].split(":")
    ok, reason = evaluate_access(plan["user"], resource, action, NOW)
    if ok:
        return "허용(" + reason + ")"
    return "거부(" + reason + ")"


def judge_all(plans):
    results = []
    for plan in plans:
        results.append(judge(plan))
    return results


before = judge_all(plans)
log = execute_revocation(plans, USERS, ROLES, EXCEPTIONS, NOW_TEXT)
after = judge_all(plans)
audited = add_audit_keys(log, plans, USERS, DECISIONS, before, after, EXECUTOR)

print("--- 감사용 이력 (키 추가)")
for entry in audited:
    print(entry["user"], entry["permission"], "|", entry["result"])
    print("   사유:", entry["reason"])
    print("   승인자:", entry["approver"], "| 실행자:", entry["executor"], "| 대상:", entry["target"])
    print("   전후:", entry["before"], "->", entry["after"])

count = save_log(audited, "revocation_log_audit.json")
saved = load_json("revocation_log_audit.json", [])
print("--- 저장")
print("저장", count, "건, 다시 읽은 건수", len(saved), "건")
print("첫 이력의 키:", list(saved[0].keys()))
