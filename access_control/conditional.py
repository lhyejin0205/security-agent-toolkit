from config_loader import load_json
from policy import evaluate_access


def load_rules(path):
    return load_json(path, [])


def is_work_time(rule, now):
    start, end = rule["hours"]
    hour = now.hour
    return start <= hour < end


def is_allowed_network(rule, network):
    allowed_networks = rule["networks"]
    return network in allowed_networks


def evaluate_conditional(user, resource, action, network, now, rules):
    ok, reason = evaluate_access(user, resource, action, now)
    if not ok:
        return False, reason
    permission = f"{resource}:{action}"
    for rule in rules:
        if rule["permission"] == permission:
            if not is_work_time(rule, now):
                return False, "업무 시간 밖"
            if not is_allowed_network(rule, network):
                return False, "허용되지 않은 접속 위치"
    return True, reason
