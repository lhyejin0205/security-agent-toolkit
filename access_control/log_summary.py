import json                                                      # JSON 문자열을 딕셔너리로 바꾸는 모듈을 불러온다

def read_log(path):                                              # 로그 파일 경로를 받는 함수
    """서버 로그 파일을 한 줄씩 읽어 요청 딕셔너리 리스트로 만든다.
    주간 로그를 집계하기 전에 파일을 읽을 때 쓴다.
    """
    entries = []                                                 # 요청 딕셔너리를 모을 리스트
    with open(path, encoding="utf-8") as log_file:                      # 파일을 연다
        for line in log_file:                                           # 파일에서 한 줄씩 꺼낸다
            entry = json.loads(line)                             # JSON 문자열을 딕셔너리로 바꾼다
            entries.append(entry)                                # 요청 리스트에 추가한다
    return entries                                               # 요청 리스트를 리턴한다

def count_by(entries, key):                                      # 요청 리스트와 센 기준(키 이름)을 받는 함수
    """요청을 key 의 값별로 세어 {값: 횟수} 딕셔너리를 리턴한다.
    사용자별 · 이유별로 몇 번인지 알고 싶을 때 쓴다.
    예: count_by(entries, "user")
    """
    counts = {}                                                  # 값별 횟수를 담을 딕셔너리
    for entry in entries:                                        # 요청을 하나씩 꺼낸다
        value = entry[key]                                       # 기준이 되는 값을 꺼낸다
        old_count = counts.get(value, 0)                         # 그 값의 지금까지 횟수(처음이면 0)
        counts[value] = old_count + 1                            # 횟수를 1 늘린다
    return counts                                                # 값별 횟수를 리턴한다

def filter_denied(entries):                                      # 요청 리스트를 받는 함수
    """거부된 요청만 모아 리스트로 리턴한다.
    거부 사유와 사용자를 따로 볼 때 쓴다.
    """
    denied = []                                                  # 거부된 요청을 모을 리스트
    for entry in entries:                                        # 요청을 하나씩 꺼낸다
        if not entry["allowed"]:                                 # 요청이 거부됐으면
            denied.append(entry)                                 # 요청을 거부 리스트에 추가한다
    return denied                                                # 거부된 요청 리스트를 리턴한다

def deny_rate(entries):                                          # 요청 리스트를 받는 함수
    """전체 요청 중 거부된 요청의 비율(0 ~ 1)을 리턴한다.
    주간 보고서에서 거부율을 구할 때 쓰며, 요청이 없으면 0.0 이다.
    """
    total = len(entries)                                         # 전체 요청 수
    if total == 0:                                               # 요청이 하나도 없으면
        return 0.0                                               # 0 으로 나눌 수 없으므로 0.0 을 리턴한다
    denied_entries = filter_denied(entries)                      # 거부된 요청 리스트
    denied = len(denied_entries)                                 # 거부된 요청 수
    return denied / total                                        # 거부 수를 전체 수로 나눈 비율을 리턴한다

def find_heavy_users(denied_counts, limit):                      # 사용자별 거부 횟수 딕셔너리와 기준 횟수를 받는 함수
    """거부 횟수가 limit 이상인 사용자 이름 리스트를 리턴한다.
    거부가 한 사람에게 몰렸는지 확인할 때 쓴다.
    """
    heavy = []                                                   # 기준에 걸린 사용자 이름을 모을 리스트
    for user, count in denied_counts.items():                    # 사용자 이름과 거부 횟수를 하나씩 꺼낸다
        if count >= limit:                                       # 거부 횟수가 기준 이상이면
            heavy.append(user)                                   # 사용자 이름을 목록에 추가한다
    return heavy                                                 # 기준에 걸린 사용자 이름을 리턴한다
