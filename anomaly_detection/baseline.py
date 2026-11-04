import pandas as pd

LOGIN_PATH = "baseline_logins.csv"


def load_daily_failures(path):
    """지난 7일의 하루 로그인 실패 횟수 파일을 표로 읽는다.
    평소 기준을 만들기 전에 맨 먼저 쓴다.
    """
    # 1. pd.read_csv 로 path 의 파일을 읽어 daily 에 담는다 (path 는 따옴표 없이 그대로 쓴다)
    daily = pd.read_csv(path)
    return daily


def average_failures(daily):
    """지난 7일 표 숫자 7개의 평균을 구한다.
    「평소 하루에 몇 번쯤 실패하는가」를 알고 싶을 때 쓴다.
    """
    # 2. daily 의 "failed_logins" 열을 꺼내 counts 에 담는다
    counts = daily["failed_logins"]
    # 3. counts 의 평균을 .mean() 으로 구해 average 에 담는다
    average = counts.mean()
    return average


def maximum_failures(daily):
    """하루 최대 로그인 실패 횟수를 구한다.
    「평소 가장 많았던 날」이 얼마나 많았는지 알고 싶을 때 쓴다.
    """
    # 4. daily 의 "failed_logins" 열을 꺼내 counts 에 담는다
    counts = daily["failed_logins"]
    # 5. counts 의 최댓값을 .max() 로 구해 maximum 에 담는다
    maximum = counts.max()
    return maximum


def make_limit(maximum):
    """평소 최댓값보다 1 큰 숫자를 알림 기준(임계값)으로 정한다.
    이 숫자 이상이면 평소보다 많다고 보고 알릴 때 쓴다.
    """
    # 6. maximum 에 1 을 더해 limit 에 담는다
    limit = maximum + 1
    return limit
