def log_line(item, action, text):
    """Create one consistent audit record."""
    entry = {
        "incident": item["id"],
        "playbook": item["playbook"],
        "action": action,
        "result": text,
    }
    return entry
