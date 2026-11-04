import json

ALERTS_PATH = "alerts.json"


def make_alert(alert_type, target, count, note):
    """알림 한 건을 딕셔너리로 만든다.
    알림마다 같은 모양으로 담아 한 파일에 모을 때 쓴다.
    """
    # 1. 알림 한 건을 키 다섯 개를 가진 딕셔너리로 만든다
    alert = {
        "type": alert_type,
        "target": target,
        "count": count,
        "note": note,
        "status": "확인 필요",
    }
    return alert


def make_login_alerts(alert_ips):
    """로그인 실패 알림 대상 주소마다 「비정상 로그인」 알림을 하나씩 만든다.
    3교시에서 추출한 주소를 알림 형식으로 바꿀 때 쓴다.
    """
    alerts = []
    for ip_address, count in alert_ips.items():
        note = "로그인 실패가 기준 이상 — 공격 확정이 아니라 먼저 살펴볼 곳"
        # 2. 로그인 실패 알림 한 건을 만든다
        alert = make_alert("비정상 로그인", ip_address, count, note)
        alerts.append(alert)
    return alerts


def make_traffic_alerts(spike_minutes):
    """요청이 급증한 분마다 「트래픽 급증」 알림을 하나씩 만든다.
    5교시에서 추출한 분을 알림 형식으로 바꿀 때 쓴다.
    """
    alerts = []
    for minute, count in spike_minutes.items():
        note = "요청이 평소의 3배 이상으로 늘어남 — 공격 확정이 아니라 먼저 살펴볼 곳"
        # 3. 시각 값을 문자열로 바꿔 target 에 담는다
        target = str(minute)
        # 4. 트래픽 급증 알림 한 건을 만든다
        alert = make_alert("트래픽 급증", target, count, note)
        alerts.append(alert)
    return alerts


def save_alerts(alerts, path):
    """알림 리스트를 JSON 파일로 저장하고 저장한 건수를 리턴한다.
    담당자와 다른 프로그램이 같은 파일로 알림을 처리하게 할 때 쓴다.
    """
    # 5. 알림 파일을 쓰기 모드로 연다
    with open(path, "w", encoding="utf-8") as file:
        # 6. 한글과 들여쓰기를 유지해 JSON 으로 저장한다
        json.dump(alerts, file, ensure_ascii=False, indent=2)
    saved_count = len(alerts)
    return saved_count
