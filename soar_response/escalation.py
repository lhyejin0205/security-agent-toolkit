from ticket_notice import send_with_retry, MAX_TRIES


def overdue_minutes(ticket, now):
    """Return how many minutes have passed since the ticket SLA deadline."""
    return now - ticket["sla_due"]


def needs_escalation(ticket, now):
    """Only open tickets past their SLA deadline need escalation."""
    if ticket["status"] != "열림":
        return False
    return overdue_minutes(ticket, now) >= 0


def pick_level(overdue, steps):
    """Return the highest escalation step reached, or zero if none applies."""
    level = 0
    for index in range(len(steps)):
        step = steps[index]
        if overdue >= step["overdue_minutes"]:
            level = index + 1
    return level


def escalate_ticket(ticket, now, rules):
    """Notify the next appropriate recipient once per escalation level."""
    overdue = overdue_minutes(ticket, now)
    steps = rules["escalation_steps"]
    level = pick_level(overdue, steps)
    if level <= ticket["escalation_level"]:
        return "그대로"
    step = steps[level - 1]
    message = "[올림 " + str(level) + "단계] " + ticket["id"] + " " + ticket["title"] + " · 기한을 " + str(overdue) + "분 넘김 · 받는 사람: " + step["notify"]
    attempt = send_with_retry(message, rules["alert_url"], MAX_TRIES)
    if attempt == 0:
        return "실패"
    ticket["escalation_level"] = level
    comment = str(now) + "분 · " + str(level) + "단계로 " + step["notify"] + " 에게 올림"
    ticket["comments"].append(comment)
    return "올림"
