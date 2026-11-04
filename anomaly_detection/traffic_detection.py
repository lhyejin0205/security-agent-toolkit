import pandas as pd

EVENTS_PATH = "normalized_events.json"
TRAFFIC_PATH = "baseline_traffic.csv"
SPIKE_MULTIPLE = 3


def load_events(path):
    """이벤트 파일을 표로 읽는다.
    분석을 시작할 때 맨 먼저 쓴다.
    """
    events = pd.read_json(path)
    return events


def add_minute_column(events):
    """이벤트마다 시각에서 초를 버린 minute 열을 붙인다.
    분당 요청 수를 세기 전에 같은 분으로 그룹화할 기준을 만들 때 쓴다.
    """
    times = pd.to_datetime(events["time"])
    # 1. times 에 .dt.floor("min") 을 붙여 초를 버린 시각을 minutes 에 담는다
    minutes = times.dt.floor("min")
    events["minute"] = minutes
    return events


def count_web_per_minute(events):
    """웹 서버 이벤트만 골라 분마다 요청이 몇 개인지 센다.
    분당 요청 수를 평소와 비교하기 전에 쓴다.
    """
    # 2. events["source"] == "web" 으로 행마다 True 또는 False 를 구해 is_web 에 담는다 (웹 서버 이벤트이면 True)
    is_web = events["source"] == "web"
    # 3. events 에서 is_web 이 True 인 행만 골라 web_events 에 담는다 (events[is_web])
    web_events = events[is_web]
    counts = web_events.groupby("minute").size()
    return counts


def make_traffic_limit(path, multiple):
    """지난 7일 분당 요청 평균의 multiple 배를 급증 기준으로 정한다.
    평소보다 요청이 크게 늘어난 분을 가려낼 급증 기준을 정할 때 쓴다.
    """
    baseline = pd.read_csv(path)
    average = baseline["requests_per_minute"].mean()
    # 4. average 에 multiple 을 곱해 limit 에 담는다
    limit = average * multiple
    return limit


def pick_spike_minutes(counts, limit):
    """요청 수가 급증 기준 이상인 분만 골라 리턴한다.
    알림을 보낼 분을 가릴 때 쓴다.
    """
    # 5. counts 가 limit 이상인지 비교한 결과(>=)를 is_spike 에 담는다
    is_spike = counts >= limit
    # 6. counts 에서 is_spike 가 True 인 것만 골라 spike_minutes 에 담는다 (counts[is_spike])
    spike_minutes = counts[is_spike]
    return spike_minutes
