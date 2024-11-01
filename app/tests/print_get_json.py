from ..src.get_books import get_pages


def print_notion_book():
    pages = get_pages()
    for page in pages:
        print()
        print("Page id: " + page["id"])
        props = page["properties"]
        for t in props["Title"]["title"]:
            name = "Title: " + t["text"]["content"]
            print(name)
        own_status = "Ownership Status: "
        for s in props["Ownership Status"]["multi_select"]:
            own_status += s["name"] + ", "
        print(own_status)
        read_status = "Reading Status: "
        for s in props["Reading Status"]["multi_select"]:
            read_status += s["name"] + ", "
        print(read_status)
