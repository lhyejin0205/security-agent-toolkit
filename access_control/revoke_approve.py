from config_loader import load_json


def load_sensitive(path):
    return load_json(path, [])


def plan_key(plan):
    user = plan["user"]
    permission = plan["permission"]
    return f"{user}:{permission}"


def needs_approval(plan, sensitive):
    is_sensitive = plan["permission"] in sensitive
    is_big_impact = plan["impact"] >= 2
    return is_sensitive or is_big_impact


def mark_approvals(plans, sensitive, decisions):
    results = []
    for plan in plans:
        item = plan.copy()
        key = plan_key(plan)
        decision = decisions.get(key)
        needs = needs_approval(plan, sensitive)
        if not needs:
            item["approval"] = "승인 불필요"
        elif decision == "승인":
            item["approval"] = "승인됨"
        else:
            item["approval"] = "승인 대기"
        results.append(item)
    return results
