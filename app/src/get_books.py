from app import DATABASE_ID, headers
import requests
import json
import os


def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    print(url)
    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    with open(os.getcwd() + "/app/files/db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    results = data["results"]
    return results
