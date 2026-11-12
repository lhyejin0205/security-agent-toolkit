import json                                                   # JSON 문자열 ↔ 딕셔너리를 바꾸는 도구
import requests                                               # 인터넷으로 요청을 보내는 도구 (9/30)

# 꼭 있어야 하는 키 네 개
REQUIRED = ["model", "approve_severity", "report_folder", "webhook_url"]
RANK = {"low": 1, "medium": 2, "high": 3}                     # 위험도 순위 — 클수록 위험하다


def load_config(path):                                        # 설정을 읽고 빠진 키가 없는지 검사하는 함수
    with open(path, encoding="utf-8") as f:                   # 설정 파일을 읽기로 연다
        config = json.load(f)                                 # 설정을 딕셔너리로 읽는다
    for key in REQUIRED:                                      # 꼭 있어야 하는 키를 하나씩
        if key not in config:                                 # 설정에 그 키가 없으면
            print("[설정 오류] 빠진 키:", key)                       # 어떤 키가 빠졌는지 알린다
            return None                                       # None 을 리턴하고 여기서 끝낸다
    return config                                             # 다 있으면 설정을 리턴한다


def needs_approval(severity, config):                         # 사람에게 확인받을 위험도인지 판정하는 함수
    level = RANK.get(severity.lower(), 3)                     # 모르는 위험도는 high 로 본다 — 놓치는 것보다 묻는 게 낫다
    return level >= RANK[config["approve_severity"]]          # 기준 이상이면 True


def notify(message, url):                                     # 메시지를 알림 서버로 보내는 함수
    # 1. try 안에서 url 로 {"text": message} 를 POST 하고(timeout=5) True 를 return 하세요
    try:
        requests.post(url, json={"text": message}, timeout=5)
        return True
    # 2. except Exception as e: 를 쓰고, 아래 출력 줄 다음에 False 를 return 하세요
    except Exception as e:
        # ── 미리 채운 줄 — except 안에 들어가도록 들여쓰기가 맞춰져 있습니다 ──
        print("[알림 실패]", type(e).__name__)                    # 에러 이름을 알린다 — 숨기지 않는다
        return False
