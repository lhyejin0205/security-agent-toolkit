import json


def load_json(path, default):
    """JSON 파일을 읽어 리턴한다. 파일이 없거나 깨졌으면 경고를 출력하고 default 를 리턴한다."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("[경고] 설정 파일 없음:", path)
        return default
    except json.JSONDecodeError:
        print("[경고] 설정 파일 깨짐:", path)
        return default
