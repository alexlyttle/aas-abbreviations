import json
from urllib.request import urlopen

ABBREVIATIONS_URL = "https://ui.adsabs.harvard.edu/help/actions/aas_macros.sty"
ABBREVIATIONS_PATH = "abbreviations.json"
TITLES_PATH = "aas_macro_titles.txt"

SKIPLINES = 36  # number of lines to skip
FORBIDDEN_WORDS = {"and", "&", "the"}

def read_url(url: str, encoding: str='utf-8') -> str:
    """Reads the content of a URL and returns it as a string."""
    with urlopen(url) as file:
        content = file.read().decode(encoding)
    return content

def read_journal_titles(path):
    """Extracts journal titles from a plain text file.
    
    Each line should separate the journal macro from the title with a tab.
    """
    titles = {}
    with open(path) as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                continue
            key, value = line.split("\t")
            titles[key] = value
    return titles

def get_journal_abbreviation(content: str, skiplines=36):
    """Extracts the journal abbreviations from the LaTeX style content string."""
    abbr = {}
    content = content.replace("~", "\u00A0")
    content = content.replace("\\&", "&")
    for line in content.strip().splitlines()[skiplines:]:
        if line.startswith("\\def"):
            key = line[4:line.find("{")]
            start = line.find("@jnl{") + 5
            end = start + line[start:].find("}")
            abbr[key] = line[start:end]
        elif line.startswith("\\let"):
            key = line[4:line.find("=")]
            abbr[key] = abbr[line[line.find("=")+1:]]
    return abbr

def clean_title(title: str, forbidden_words: set={}) -> str:
    """Removes forbidden words from a title and returns it as a lowercase string."""
    words = title.lower().split()
    return " ".join([word for word in words if word not in forbidden_words])

def get_container_title(abbreviations: dict, journal_titles: dict, forbidden_words: set={}) -> dict:
    """Extracts the abbreviation container titles from the LaTeX style content string."""
    containter_title = {}
    for key in journal_titles:
        if key in abbreviations:
            new_key = clean_title(journal_titles[key], forbidden_words=forbidden_words)
            containter_title[new_key] = abbreviations[key]
    return containter_title

def update_container_title(path: str, container_title: dict) -> None:
    """Updates the container titles dictionary in the json file at path."""
    with open(path) as file:
        abbreviations = json.loads(file.read())

    abbreviations["default"]["container-title"] = container_title
    content = json.dumps(abbreviations, indent=4)

    with open(path, "w") as file:
        file.write(content)
    
def main() -> None:
    content = read_url(ABBREVIATIONS_URL)
    abbreviations = get_journal_abbreviation(content, skiplines=SKIPLINES)
    journal_titles = read_journal_titles(TITLES_PATH)
    container_title = get_container_title(abbreviations, journal_titles, forbidden_words=FORBIDDEN_WORDS)
    update_container_title(ABBREVIATIONS_PATH, container_title)

if __name__ == "__main__":
    main()
