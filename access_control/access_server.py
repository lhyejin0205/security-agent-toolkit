import json
from datetime import datetime
from flask import Flask, request
from conditional import load_rules, evaluate_conditional

app = Flask(__name__)
app.json.ensure_ascii = False
RULES = load_rules("config/conditions.json")
LOG_PATH = "server_log.jsonl"
TIME_FORMAT = "%Y-%m-%dT%H:%M"


def parse_time(text):
    if text is None:
        return None
    try:
        return datetime.strptime(text, TIME_FORMAT)
    except ValueError:
        return None


def write_log(entry):
    mode = "a"
    with open(LOG_PATH, mode, encoding="utf-8") as f:
        text = json.dumps(entry, ensure_ascii=False)
        f.write(text + "\n")


@app.route("/check")
def check():
    user = request.args.get("user")
    resource = request.args.get("resource")
    action = request.args.get("action")
    network = request.args.get("network")
    time_text = request.args.get("time")
    now = parse_time(time_text)
    if None in (user, resource, action, network, now):
        return {"allowed": False, "reason": "입력이 잘못됨"}, 400
    allowed, reason = evaluate_conditional(user, resource, action, network, now, RULES)
    log_entry = {
        "time": request.args.get("time"),
        "user": user,
        "permission": f"{resource}:{action}",
        "network": network,
        "allowed": allowed,
        "reason": reason,
    }
    write_log(log_entry)
    if allowed:
        return {"allowed": True, "reason": reason}, 200
    return {"allowed": False, "reason": reason}, 403

if __name__ == "__main__":
    app.run(port=5001)
