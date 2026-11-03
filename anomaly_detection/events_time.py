import pandas as pd

EVENTS_PATH = "normalized_events.json"
FAILED_PATH = "failed_events.csv"


def load_events(path):
    """이벤트 파일을 표로 읽는다.
    분석을 시작할 때 맨 먼저 쓴다.
    """
    events = pd.read_json(path)
    return events


def pick_failed(events):
    """실패한 이벤트만 골라 새 표로 만든다.
    무엇이 잘못됐는지 조사할 때 성공한 이벤트는 빼고 보는 데 쓴다.
    """
    results = events["result"]
    is_fail = results == "실패"
    failed = events[is_fail]
    return failed


def count_by_user(failed):
    """실패 횟수를 사용자별로 세어 많은 순서로 리턴한다.
    누구에게 실패가 많이 났는지 볼 때 쓴다.
    """
    grouped = failed.groupby("user")
    counts = grouped.size()
    sorted_counts = counts.sort_values(ascending=False)
    return sorted_counts


def add_hour(events):
    """time 열을 시각으로 바꾸고 「시」만 담은 hour 열을 더한다.
    시간대별로 세기 전에 쓴다.
    """
    times = pd.to_datetime(events["time"])
    hours = times.dt.hour
    events["hour"] = hours
    return events


def count_by_hour(failed):
    """실패 횟수를 시간대별로 센다.
    실패가 몇 시에 많이 났는지 볼 때 쓴다.
    """
    grouped = failed.groupby("hour")
    counts = grouped.size()
    return counts


def save_failed(failed, path):
    """실패한 이벤트 표를 CSV 파일로 저장한다.
    담당자가 엑셀로 근거를 확인하게 할 때 쓴다.
    """
    columns = ["time", "source", "user", "ip", "action", "result", "hour"]
    failed[columns].to_csv(path, index=False)
