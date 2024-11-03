from ..src.update_books import update_page


def update_title(new_title):
    page_id = "3c4d157e-4303-4eb0-a8c8-ac9e81510dea"
    update_data = {"Title": {"title": [{"text": {"content": new_title}}]}}
    update_page(page_id, update_data)
