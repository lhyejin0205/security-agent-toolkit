import json
from normalize_web import normalize_web
from normalize_json_csv import load_server, load_saas

EVENTS_PATH = "normalized_events.json"


def load_web(path):
    """웹 서버 로그 파일의 모든 줄을 공통 이벤트 리스트로 바꾸고 깨진 줄은 건너뛴다."""
    events = []
    with open(path, encoding="utf-8") as web_file:
        for line in web_file:
            event = normalize_web(line)
            if event is not None:
                events.append(event)
    return events


def get_time(event):
    """정렬 기준으로 쓸 시각 문자열을 리턴한다."""
    return event["time"]


def merge_events(web, server, saas):
    """이벤트 리스트 세 개를 하나로 이어 붙이고 시간순으로 정렬한다."""
    events = web + server + saas
    events.sort(key=get_time)
    return events


def count_by_source(events):
    """소스별 이벤트 수를 {소스: 개수} 딕셔너리로 센다."""
    counts = {}
    for event in events:
        source = event["source"]
        counts[source] = counts.get(source, 0) + 1
    return counts


def count_missing(events, key):
    """key 키의 값이 비어 있는(None) 이벤트 수를 리턴한다."""
    missing = 0
    for event in events:
        if event[key] is None:
            missing = missing + 1
    return missing


def save_events(events, path):
    """이벤트 리스트를 JSON 파일로 저장한다."""
    with open(path, "w", encoding="utf-8") as events_file:
        json.dump(events, events_file, ensure_ascii=False, indent=2)
