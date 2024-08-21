from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/jason",
    "Notion-Version": "2022-06-28",
}


def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    with open("db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    results = data["results"]
    return results


pages = get_pages()
for page in pages:
    props = page["properties"]
    title = props["Name"]["title"]
    for t in title:
        name = t["text"]["content"]
        print(name)
