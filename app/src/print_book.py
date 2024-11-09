def print_book(data):
    print()
    _print_isbn(data)
    _print_if_text(data, "cover", "Cover URL: ")
    _print_if_text(data, "Title", "Title: ")
    _print_if_text(data, "Subtitle", "Subtitle: ")
    _print_if_list(data, "Author", "Authors:")
    _print_if_list(data, "Editor", "Editors:")
    _print_if_list(data, "Illustrator", "Illustrators:")
    _print_if_list(data, "Translator", "Translators:")
    _print_if_list(data, "Publisher", "Publishers:")
    _print_if_list(data, "Imprint", "Imprints:")
    _print_if_list(data, "Series", "Series:")
    _print_if_list(data, "Format", "Formats:")
    _print_if_list(data, "Genres", "Genres:")
    _print_if_number(data, "First Pub. Year", "First Pub. Year: ")
    _print_if_number(data, "Publication Year", "Publication Year: ")
    _print_if_list(data, "Setting Places", "Setting Places:")
    _print_if_list(data, "Setting Times", "Setting Times:")
    _print_if_list(data, "Language", "Languages:")
    _print_if_number(data, "Pages", "Pages: ")
    _print_if_number(data, "Weight", "Weight: ")
    _print_if_number(data, "Width", "Width: ")
    _print_if_number(data, "Height", "Height: ")
    _print_if_number(data, "Spine Width", "Height: ")


def _print_isbn(data):
    if "ISBN" in data:
        print("ISBN: " + data["ISBN"]["title"][0]["text"]["content"])


def _print_if_text(data, name, text):
    if name in data:
        print(text + data[name]["rich_text"][0]["text"]["content"])


def _print_if_number(data, name, text):
    if name in data:
        print(text + str(data[name]["number"]))


def _print_if_list(data, name, text):
    if name in data:
        multi = data[name]["multi_select"]
        if len(multi) > 0:
            print(text)
            for i in range(len(multi)):
                print("\t" + multi[i]["name"])
