from datetime import datetime
from conditional import load_rules, evaluate_conditional

TIME_FORMAT = "%Y-%m-%d %H:%M"
RULES = load_rules("config/conditions.json")

CASES = [
    ("seoyeon", "SALES", "QUERY", "office", "2026-10-30 10:00"),
    ("seoyeon", "SALES", "CHANGE", "office", "2026-10-30 09:00"),
    ("seoyeon", "SALES", "CHANGE", "office", "2026-10-30 18:00"),
    ("seoyeon", "SALES", "CHANGE", "external", "2026-10-30 10:00"),
    ("seoyeon", "SALES", "CHANGE", "external", "2026-10-30 22:00"),
    ("junho", "SETTLE", "QUERY", "vpn", "2026-10-30 19:30"),
    ("gaeun", "ACCOUNT", "CHANGE", "vpn", "2026-10-30 10:00"),
    ("dami", "SALES", "QUERY", "office", "2026-10-30 10:00"),
]

print("--- 단계 1: 판정 - 요청", len(CASES), "건")
number = 0
for user, resource, action, network, time_text in CASES:
    number += 1
    now = datetime.strptime(time_text, TIME_FORMAT)
    ok, reason = evaluate_conditional(user, resource, action, network, now, RULES)
    if ok:
        result = "허용"
    else:
        result = "거부"
    permission = f"{resource}:{action}"
    time_text = now.strftime("%H:%M")
    verdict = f"{result}({reason})"
    print(number, user, permission, network, time_text, "->", verdict)

print("--- 단계 2: 확인 - 조건 파일에 적힌 조건")
for rule in RULES:
    hours = rule["hours"]
    hours_text = f"{hours[0]}시부터 {hours[1]}시 전까지"
    networks_text = ", ".join(rule["networks"])
    print(rule["permission"], "|", hours_text, "|", networks_text)
