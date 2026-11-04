import pandas as pd

EVENTS_PATH = "normalized_events.json"
TYPE_ORDER = ["비정상 로그인", "비인가 접근", "기타 실패", "정상"]


def load_events(path):
    """이벤트 파일을 표로 읽는다.
    분석을 시작할 때 맨 먼저 쓴다.
    """
    events = pd.read_json(path)
    return events


def classify_event(action, result):
    """이벤트 하나의 유형 이름을 정한다.
    알림이 온 이벤트가 어떤 유형의 일인지 담당자가 바로 알 수 있게 할 때 쓴다.
    """
    # 1. if 로 시작한다: result 가 "실패" 이고(and) action 이 "POST /login" 과 같으면
    if result == "실패" and action == "POST /login":
        # 2.   그 if 안쪽에서 "비정상 로그인" 을 리턴한다
        return "비정상 로그인"
    # 3. if 로 시작한다: result 가 "실패" 이고(and) "/admin" in action 이 True 이면
    if result == "실패" and "/admin" in action:
        # 4.   그 if 안쪽에서 "비인가 접근" 을 리턴한다
        return "비인가 접근"
    if result == "실패":
        return "기타 실패"
    return "정상"


def count_types(events):
    """유형별 이벤트 수를 {유형: 개수} 딕셔너리로 센다.
    어떤 유형의 일이 얼마나 있는지 한눈에 볼 때 쓴다.
    """
    # 5. events.to_dict("records") 로 표를 딕셔너리 리스트로 바꿔 event_list 에 담는다
    event_list = events.to_dict("records")
    counts = {}
    for event in event_list:
        action = event["action"]
        result = event["result"]
        type_name = classify_event(action, result)
        counts[type_name] = counts.get(type_name, 0) + 1
    return counts
