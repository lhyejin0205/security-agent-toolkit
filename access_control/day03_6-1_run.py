from datetime import datetime

from config_loader import load_json
from req_create import REQUESTS, create_request
from req_review import approve_request, reject_request
from req_grant import grant_request
from req_sla import check_sla_breach
from request_flow import save_requests, count_by_status

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

print("--- 단계 1: 처리 - 승인 · 반려 · 부여")
approve_request(REQUESTS[0], "security_manager")
reject_request(REQUESTS[1], "security_manager")
approve_request(REQUESTS[2], "security_manager")
approve_request(REQUESTS[3], "security_manager")
for request in REQUESTS:
    ok, result = grant_request(request)
    print(request["id"], request["user"], request["status"], "->", result)

print("--- 단계 2: 점검 - 상태별 건수와 SLA")
print(count_by_status(REQUESTS))
for request in check_sla_breach(REQUESTS, NOW):
    print("SLA 초과 요청 번호:", request["id"])

print("--- 단계 3: 저장 - requests.json")
count = save_requests(REQUESTS, "requests.json")
print("저장 함수가 리턴한 건수:", count)
saved = load_json("requests.json", [])
print("저장한 요청서", len(saved), "건, 첫 요청서의 상태:", saved[0]["status"])
