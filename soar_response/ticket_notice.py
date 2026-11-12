from notifier import notify

MAX_TRIES = 3


def pick_recipients(grade, rules):
    """등급에 맞는 수신자 이름 리스트를 리턴한다."""
    table = rules["recipients"]
    return table[grade]


def should_send(ticket, now, gap):
    """처음 알리거나 최소 간격이 지난 경우에만 전송한다."""
    if ticket["notified_count"] == 0:
        return True
    elapsed = now - ticket["last_notified"]
    return elapsed >= gap


def send_with_retry(message, url, max_tries):
    """성공할 때까지 최대 횟수만큼 보내고 성공한 시도 번호를 리턴한다."""
    for attempt in range(1, max_tries + 1):
        if notify(message, url):
            return attempt
    return 0


def send_ticket_notice(ticket, now, rules):
    """티켓 알림을 보내고 전송, 건너뜀, 실패 중 하나를 리턴한다."""
    if not should_send(ticket, now, rules["send_gap_minutes"]):
        return "건너뜀"
    recipients = pick_recipients(ticket["grade"], rules)
    names = ""
    for name in recipients:
        if names != "":
            names = names + ", "
        names = names + name
    message = ticket["title"] + " · " + ticket["id"] + " · 알림 " + str(ticket["count"]) + "건 · 기한 " + str(ticket["sla_due"]) + "분 · 수신: " + names
    attempt = send_with_retry(message, rules["alert_url"], MAX_TRIES)
    if attempt == 0:
        return "실패"
    ticket["notified_count"] = ticket["notified_count"] + 1
    ticket["last_notified"] = now
    return "전송"
