import json
import os
import requests

BASE_URL = "http://127.0.0.1:5001"
LOG_PATH = "server_log.jsonl"
CASES = [
    {"user": "seoyeon", "resource": "SALES", "action": "CHANGE", "network": "office", "time": "2026-10-30T09:00"},
    {"user": "seoyeon", "resource": "SALES", "action": "CHANGE", "network": "office", "time": "2026-10-30T18:00"},
    {"user": "seoyeon", "resource": "SALES", "action": "CHANGE", "network": "external", "time": "2026-10-30T10:00"},
    {"user": "seoyeon", "resource": "SALES", "action": "QUERY", "network": "external", "time": "2026-10-30T23:00"},
    {"user": "junho", "resource": "SETTLE", "action": "QUERY", "network": "vpn", "time": "2026-10-30T19:30"},
    {"user": "junho", "resource": "SETTLE", "action": "QUERY", "network": "external", "time": "2026-10-30T10:00"},
    {"user": "gaeun", "resource": "ACCOUNT", "action": "CHANGE", "network": "vpn", "time": "2026-10-30T10:00"},
    {"user": "dami", "resource": "SALES", "action": "QUERY", "network": "office", "time": "2026-10-30T10:00"},
    {"user": "seoyeon", "resource": "SALES", "action": "CHANGE", "time": "2026-10-30T10:00"},
]

if os.path.exists(LOG_PATH):
    os.remove(LOG_PATH)

print("--- 단계 1: 응답 - 요청", len(CASES), "건")
results = []
case_count = len(CASES)
for i in range(case_count):
    case = CASES[i]
    response = requests.get(BASE_URL + "/check", params=case)
    body = response.json()
    result = {
        "status": response.status_code,
        "allowed": body["allowed"],
        "reason": body["reason"],
    }
    results.append(result)
    permission = case["resource"] + ":" + case["action"]
    print(i + 1, case["user"], permission, "->", response.status_code, body["reason"])

entries = []
with open(LOG_PATH, encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        entries.append(entry)
print("--- 단계 2: 로그 - 서버가 남긴", len(entries), "줄")
for entry in entries:
    print(entry["user"], entry["permission"], entry["network"], entry["time"], "->", entry["allowed"], entry["reason"])

answered = 0
for result in results:
    if result["status"] != 400:
        answered = answered + 1
print("--- 단계 3: 대조 - 판정까지 간 응답과 로그")
print("판정까지 간 응답", answered, "건 / 로그에 남은 줄", len(entries), "줄")
