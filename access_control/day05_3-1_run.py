from rbac import USERS, ROLES
from revoke_input import load_to_revoke
from revoke_plan import plan_revocation
from revoke_approve import load_sensitive, mark_approvals

DECISIONS = {"dami:SALES:QUERY": "승인", "dami:SALES:CHANGE": "승인"}

to_revoke = load_to_revoke()
plans = plan_revocation(to_revoke, USERS, ROLES)
sensitive = load_sensitive("config/sensitive.json")
results = mark_approvals(plans, sensitive, DECISIONS)

print("--- 단계 1: 승인 상태 - 계획 8건")
for item in results:
    print(item["user"], item["permission"], "<-", item["source"], "|", item["method"], "| 영향", item["impact"], "건 |", item["approval"])

print("--- 단계 2: 집계 - 승인 상태별 건수")
counts = {}
for item in results:
    count_key = item["approval"]
    old_count = counts.get(count_key, 0)
    counts[count_key] = old_count + 1
print(counts)
