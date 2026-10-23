from datetime import datetime

from config_loader import load_json
from exception_policy import TIME_FORMAT

SLA_HOURS = load_json("config/sla.json", {"hours": 4})["hours"]


def check_sla_breach(requests, now):
    """검토 중(reviewing)인 요청서 가운데 접수한 지 SLA_HOURS 시간을 초과한 것의 목록을 리턴한다."""
    breached = []
    for request in requests:
        if request["status"] == "reviewing":
            requested = datetime.strptime(request["requested_at"], TIME_FORMAT)
            hours = (now - requested).total_seconds() / 3600
            if hours > SLA_HOURS:
                overdue = request.copy()
                overdue["wait_hours"] = round(hours, 1)
                breached.append(overdue)
    return breached
