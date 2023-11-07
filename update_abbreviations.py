import os, json
from html2text import html2text
from urllib.request import urlopen

URL = "https://adsabs.harvard.edu/abs_doc/journals1.html"
PATH = "abbreviations.json"
HEADER = 16  # number of lines in page header
COLUMN = 13  # location of column divider
FORBIDDEN_WORDS = {"and", "&", "the"}

def read_url(url: str, encoding: str='utf-8') -> str:
    """Reads the content of a URL and returns it as a string."""
    with urlopen(url) as file:
        content = file.read().decode(encoding)
    return content

def clean_title(title: str, forbidden_words: set={}) -> str:
    """Removes forbidden words from a title and returns it as a lowercase string."""
    words = title.lower().split()
    return " ".join([word for word in words if word not in forbidden_words])

def get_container_title(content: str, header: int, column: int, forbidden_words: set={}) -> dict:
    """Extracts the abbreviation container titles from the HTML content string."""
    container_title = {}
    for i, line in enumerate(html2text(content).splitlines()):
        line = line.strip()
        if i < header or line == '':
            continue

        key = clean_title(line[column:], forbidden_words=forbidden_words)
        container_title[key] = line[:column].rstrip()
    return container_title

def update_container_title(path: str, container_title: dict) -> None:
    """Updates the container titles dictionary in the json file at path."""
    with open(path) as file:
        abbreviations = json.loads(file.read())

    abbreviations["default"]["container-title"] = container_title
    content = json.dumps(abbreviations, ensure_ascii=False, indent=4)

    with open(path, "w") as file:
        file.write(content)
    
def main() -> None:
    content = read_url(URL)
    container_title = get_container_title(content, HEADER, COLUMN, forbidden_words=FORBIDDEN_WORDS)
    update_container_title(PATH, container_title)

if __name__ == "__main__":
    main()
