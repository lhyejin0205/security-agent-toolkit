from datetime import datetime
from rbac import USERS, ROLES
from exception_policy import EXCEPTIONS, TIME_FORMAT
from policy import evaluate_access
from config_loader import load_json
from revoke_input import load_to_revoke
from revoke_plan import plan_revocation
from revoke_approve import load_sensitive, mark_approvals
from revoke import execute_revocation, save_log

NOW_TEXT = "2026-10-30 10:00"
NOW = datetime.strptime(NOW_TEXT, TIME_FORMAT)
DECISIONS = {"dami:SALES:QUERY": "승인", "dami:SALES:CHANGE": "승인"}

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
        verdict = judge(plan)
        results.append(verdict)
    return results


before = judge_all(plans)
log = execute_revocation(plans, USERS, ROLES, EXCEPTIONS, NOW_TEXT)
after = judge_all(plans)

print("--- 단계 1: 실행 - 회수 결과")
done = 0
for entry in log:
    print(entry["user"], entry["permission"], "|", entry["method"], "|", entry["result"])
    if entry["result"] == "실행":
        done = done + 1
print("실행", done, "건, 대기", len(log) - done, "건")

print("--- 단계 2: 확인 - 회수 전후의 판정")
plan_count = len(plans)
for i in range(plan_count):
    mark = "그대로"
    if before[i] != after[i]:
        mark = "바뀜"
    print(plans[i]["user"], plans[i]["permission"], "|", before[i], "->", after[i], "|", mark)

print("--- 단계 3: 저장 - 회수 이력")
count = save_log(log, "revocation_log.json")
saved = load_json("revocation_log.json", [])
print("저장", count, "건, 다시 읽은 건수", len(saved), "건, 첫 이력:", saved[0]["user"], saved[0]["permission"], saved[0]["result"])
