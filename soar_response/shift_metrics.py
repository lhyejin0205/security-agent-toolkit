def average(numbers):
    """Return the arithmetic mean, or zero for an empty list."""
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)


def collect_response_times(tickets):
    """Collect minutes from ticket creation to first acknowledgement."""
    times = []
    for ticket in tickets:
        if ticket["acked_at"] != -1:
            times.append(ticket["acked_at"] - ticket["created_at"])
    return times


def collect_resolve_times(tickets):
    """Collect minutes from ticket creation to resolution."""
    times = []
    for ticket in tickets:
        if ticket["resolved_at"] != -1:
            times.append(ticket["resolved_at"] - ticket["created_at"])
    return times


def count_sla_breaches(tickets, now):
    """Count tickets acknowledged after their SLA deadline."""
    late = 0
    for ticket in tickets:
        checked_time = ticket["acked_at"]
        if checked_time == -1:
            checked_time = now
        if checked_time > ticket["sla_due"]:
            late = late + 1
    return late
