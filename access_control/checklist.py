import json
from datetime import datetime                                    # 문자열을 시각으로 바꾸는 데 쓴다

TIME_FORMAT = "%Y-%m-%d %H:%M"                                   # 만료 시각 문자열의 형식 (예: 2026-11-03 18:00)

def load_state(path):                                            # 파일 경로를 받는 함수
    """점검할 데이터(사용자 · 역할의 부서 · 예외)를 읽어 딕셔너리로 리턴한다.
    정기 점검을 시작할 때 쓴다.
    """
    with open(path, encoding="utf-8") as json_file:                      # 파일을 연다
        return json.load(json_file)                                      # 읽은 내용을 바로 리턴한다

def check_employed(users):                                       # 사용자 딕셔너리를 받는 함수
    """퇴사했는데 계정이 남아 있는 사용자 이름 리스트를 리턴한다.
    정기 점검에서 퇴사자 계정을 찾을 때 쓴다.
    """
    problems = []                                                # 문제가 있는 사용자 이름을 모을 리스트
    for name, info in users.items():                             # 사용자 이름과 사용자 항목을 하나씩 꺼낸다
        if not info["employed"]:                                 # 재직 상태가 거짓이면
            problems.append(name)                                # 사용자 이름을 문제 리스트에 추가한다
    return problems                                              # 문제가 있는 사용자 이름을 리턴한다

def check_expired(exceptions, now):                              # 예외 리스트와 지금 시각(datetime)을 받는 함수
    """만료 시각이 지났는데 남아 있는 예외의 번호 리스트를 리턴한다.
    정기 점검에서 기간이 끝난 예외를 찾을 때 쓴다.
    """
    problems = []                                                # 문제가 있는 예외 번호를 모을 리스트
    for exception in exceptions:                                       # 예외를 하나씩 꺼낸다
        expires_at = datetime.strptime(exception["expires"], TIME_FORMAT)  # 만료 문자열을 시각으로 바꾼다
        if expires_at <= now:                                    # 만료 시각이 지금과 같거나 이전이면
            problems.append(exception["id"])                     # 예외 번호를 문제 리스트에 추가한다
    return problems                                              # 문제가 있는 예외 번호를 리턴한다

def check_dept(users, role_dept):                                # 사용자 딕셔너리와 역할별 부서 딕셔너리를 받는 함수
    """부서가 역할의 부서와 다른 사용자 이름 리스트를 리턴한다.
    정기 점검에서 엉뚱한 부서에 역할이 남은 사람을 찾을 때 쓴다.
    """
    problems = []                                                # 문제가 있는 사용자 이름을 모을 리스트
    for name, info in users.items():                             # 사용자 이름과 사용자 항목을 하나씩 꺼낸다
        expected_dept = role_dept[info["role"]]                  # 역할에 해당하는 기준 부서를 찾는다
        if expected_dept != info["dept"]:                        # 기준 부서와 사용자의 부서가 다르면
            problems.append(name)                                # 사용자 이름을 문제 리스트에 추가한다
    return problems                                              # 문제가 있는 사용자 이름을 리턴한다

def run_checklist(state, now):                                   # 읽은 데이터와 지금 시각을 받는 함수
    """점검 세 가지를 실행한다.
    점검 이름과 문제 리스트를 담은 딕셔너리의 리스트를 리턴한다.
    매주 어긋난 곳을 한 번에 찾을 때 쓴다.
    """
    users = state["users"]                                       # 사용자 딕셔너리를 꺼낸다
    exceptions = state["exceptions"]                             # 예외 리스트를 꺼낸다
    role_dept = state["role_dept"]                               # 역할별 부서 딕셔너리를 꺼낸다
    results = []                                                 # 점검 결과를 모을 리스트
    results.append({"name": "퇴사자 계정 점검", "problems": check_employed(users)})            # 첫째 점검 결과를 추가한다
    results.append({"name": "만료 예외 점검", "problems": check_expired(exceptions, now)})     # 둘째 점검 결과를 추가한다
    results.append({"name": "부서와 역할 점검", "problems": check_dept(users, role_dept)})     # 셋째 점검 결과를 추가한다
    return results                                               # 점검 결과 리스트를 리턴한다
