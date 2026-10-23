import json


def save_requests(requests, path):
    """요청서 목록을 JSON 파일로 저장한다. 한글이 그대로 보이게 쓴다."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(requests, f, ensure_ascii=False, indent=2)
    return len(requests)


def count_by_status(requests):
    """상태(status)별 요청서 건수를 딕셔너리로 리턴한다."""
    counts = {}
    for request in requests:
        status = request["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts
