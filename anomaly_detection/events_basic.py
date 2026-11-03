import pandas as pd

EVENTS_PATH = "normalized_events.json"


def load_events(path):
    """이벤트 파일을 표로 읽는다.
    분석을 시작할 때 맨 먼저 쓴다.
    """
    events = pd.read_json(path)
    return events


def describe_events(events):
    """표의 크기와 앞 시각 3개를 구한다.
    새 파일을 받았을 때 내용이 제대로 들어 있는지 확인하는 데 쓴다.
    """
    shape = events.shape
    times = events["time"]
    first_times = times.head(3)
    return shape, first_times


def pick_failed(events):
    """실패한 이벤트만 골라 새 표로 만든다.
    무엇이 잘못됐는지 조사할 때 성공한 이벤트는 빼고 보는 데 쓴다.
    """
    results = events["result"]
    is_fail = results == "실패"
    failed = events[is_fail]
    return failed


def count_values(table, column):
    """한 열의 값별 개수를 센다.
    소스별 · 결과별 · 사용자별로 몇 개인지 알고 싶을 때 쓴다.
    """
    values = table[column]
    counts = values.value_counts()
    return counts
