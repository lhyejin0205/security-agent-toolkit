from datetime import datetime

from req_create import REQUESTS, create_request
from req_review import approve_request
from req_sla import SLA_HOURS, check_sla_breach

NOW = datetime.strptime("2026-10-23 14:00", "%Y-%m-%d %H:%M")

INBOX = [
    ("seoyeon", "SETTLE", "QUERY", "2026-10-27 18:00", "정산 대조 지원", "2026-10-23 08:30"),
    ("gaeun", "SALES", "QUERY", "2026-10-28 18:00", "감사 자료 대응", "2026-10-23 10:30"),
    ("dami", "SALES", "QUERY", "2026-10-27 18:00", "인수인계 자료 확인", "2026-10-23 12:00"),
    ("junho", "SETTLE", "QUERY", "2026-10-27 18:00", "정산 확인", "2026-10-23 09:00"),
    ("seoyeon", "ACCOUNT", "QUERY", "2026-10-27 18:00", "계정 권한 점검", "2026-10-23 07:50"),
    ("tester", "SALES", "QUERY", "2026-10-27 18:00", "시험 계정 확인", "2026-10-23 10:00"),
]
for user, resource, action, until, reason, received_at in INBOX:
    create_request(user, resource, action, until, reason, received_at)
approve_request(REQUESTS[3], "security_manager")

print("--- 단계 1: 현황 - SLA 시간", SLA_HOURS, "시간, 지금 14:00")
for request in REQUESTS:
    print(request["id"], request["user"], request["status"], request["requested_at"])

print("--- 단계 2: 판정 - SLA 를 초과한 요청")
for request in check_sla_breach(REQUESTS, NOW):
    print(request["id"], request["user"], "접수", request["requested_at"], "->", request["wait_hours"], "시간 지남")
