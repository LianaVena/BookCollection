import requests
from app import headers


def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": data}
    result = requests.patch(url, json=payload, headers=headers)
    print(result.reason)
    return result
