import logging
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

logging.basicConfig(format="LOG %(asctime)s: %(message)s", level=logging.INFO)
