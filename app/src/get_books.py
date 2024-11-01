import json
import os
import requests
from app import DATABASE_ID, headers


def get_pages(payload: dict):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def get_all_pages():
    data = get_pages({"page_size": 100})
    with open(os.getcwd() + "/app/files/db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    results = data["results"]
    return results


def check_duplicate(title: str):
    data = get_pages({"filter": {"property": "Title", "title": {"equals": title}}})
    return len(data["results"]) > 0
