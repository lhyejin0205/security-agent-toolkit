def collect_failures(action_log):
    """Return audit entries whose result indicates a final failure."""
    failures = []
    for entry in action_log:
        if entry["result"].startswith("실패"):
            failures.append(entry)
    return failures
