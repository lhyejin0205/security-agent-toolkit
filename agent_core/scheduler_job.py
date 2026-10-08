import argparse
import json
import os
import schedule
import time

parser = argparse.ArgumentParser(description="정기 점검 작업")
parser.add_argument("--every", type=int, default=2, help="몇 초마다 돌릴지")
args = parser.parse_args()

THRESHOLD = 3


def load_done():
    if os.path.exists("processed_ids.json"):
        with open("processed_ids.json", encoding="utf-8") as f:
            return json.load(f)
    return []


def job():
    with open("normalized_logs.json", encoding="utf-8") as f:
        rows = json.load(f)

    count = {}                                # 룰 ① — 계정마다 실패 횟수를 센다 (9/29)
    for row in rows:
        if row["level"] == "WARN":
            user = row["user"]
            if user in count:
                count[user] = count[user] + 1
            else:
                count[user] = 1

    done = load_done()
    sent = 0

    for user in count:
        if count[user] >= THRESHOLD:
            event_id = f"brute_force:{user}"
             if event_id not in done:
                print("[전송]", event_id)
                done.append(event_id)
                sent = sent + 1



    with open("processed_ids.json", "w", encoding="utf-8") as f:
        json.dump(done, f, ensure_ascii=False, indent=2)

    print(f"점검 완료 — 새 경보 {sent}건")

for i in range(4):
    schedule.run_pending()
    time.sleep(1)

with open("scheduler_job.py", "w", encoding="utf-8") as f:
    f.write(code)

import os

if os.path.exists("processed_ids.json"):
    os.remove("processed_ids.json")
    print("processed_ids.json 을 비웠습니다 — 6교시 기록이 남아 있으면 1회차가 0건이 됩니다")

print("scheduler_job.py 를 만들었습니다. 터미널에서 python scheduler_job.py 를 두 번 실행해 보세요.")
