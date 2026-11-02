def split_request(line):                           # 로그 한 줄(문자열)을 받는 함수
    """로그 한 줄을 큰따옴표 기준으로 앞 · 요청 · 뒤 세 조각으로 나눈다.
    한 덩어리 문자열인 로그에서 값을 꺼내기 시작할 때 쓴다.
    """
    prefix, request_text, suffix = line.split('"', 2)  # 큰따옴표 두 개를 기준으로 앞 · 요청 · 뒤 세 조각으로 나눈다
    return prefix, request_text, suffix            # 세 조각을 리턴한다


def read_request(request_text):                    # 요청 조각(예: GET /login HTTP/1.1)을 받는 함수
    """요청 조각에서 방법(method)과 경로(path)를 꺼낸다.
    무엇을 요청했는지 알고 싶을 때 쓴다.
    """
    method, path, protocol = request_text.split()  # 공백 기준으로 나눈 세 값을 세 이름에 한꺼번에 담는다
    return method, path                            # 방법과 경로를 리턴한다


def read_status(suffix):                           # 요청 뒤 조각(예:  401 312 "-" "Mozilla/5.0")을 받는 함수
    """요청 뒤 조각에서 상태 코드를 꺼내 정수로 리턴한다.
    요청이 성공했는지 실패했는지 가를 때 쓴다.
    """
    parts = suffix.split()                         # 공백 기준으로 나눈 조각 리스트를 만든다
    status_text = parts[0]                         # 첫 조각이 상태 코드 문자열이다
    status = int(status_text)                      # 숫자로 바꿔야 400 이상인지 비교할 수 있다
    return status                                  # 상태 코드(정수)를 리턴한다


def read_client(prefix):                           # 요청 앞 조각(예: 203.0.113.50 - - [02/Nov/2026:09:12:03 +0900] )을 받는 함수
    """요청 앞 조각에서 접속자 주소를 꺼낸다.
    어느 주소가 요청했는지 알고 싶을 때 쓴다.
    """
    parts = prefix.split()                         # 공백 기준으로 나눈 조각 리스트를 만든다
    client_ip = parts[0]                           # 첫 조각이 접속자 주소이다
    return client_ip                               # 접속자 주소를 리턴한다


def parse_line(line):                              # 로그 한 줄을 받는 함수
    """로그 한 줄을 ip · method · path · status 딕셔너리로 바꾼다.
    깨진 줄이면 None 을 리턴한다.
    접속 로그를 분석하기 전에 한 줄을 값으로 나눌 때 쓴다.
    """
    if line.count('"') < 2:                        # 큰따옴표가 두 개보다 적은 줄이면(잘렸거나 깨진 줄이면)
        return None                                # 읽을 수 없으니 None 을 리턴한다
    prefix, request_text, suffix = split_request(line)  # 세 조각으로 나눈다
    method, path = read_request(request_text)      # 요청 조각에서 방법과 경로를 꺼낸다
    status = read_status(suffix)                   # 뒤 조각에서 상태 코드를 꺼낸다
    client_ip = read_client(prefix)                # 앞 조각에서 접속자 주소를 꺼낸다
    entry = {                                      # 꺼낸 값을 딕셔너리로 묶는다
        "ip": client_ip,                           # 접속자 주소
        "method": method,                          # 요청 방법
        "path": path,                              # 요청 경로
        "status": status,                          # 상태 코드(정수)
    }
    return entry                                   # 딕셔너리를 리턴한다
