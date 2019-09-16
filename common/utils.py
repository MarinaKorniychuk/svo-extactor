import re
from datetime import datetime
from pathlib import Path

from scrapy.utils.project import get_project_settings

from facts.settings import FEED_URI_TEMPLATE

BRACKETS_REGEX = re.compile(" \(.*?\)")
ABBR_REGEX = re.compile(" [—–] [\w/&]+|[—–][a-z]+")

PATTERNS_TO_REMOVE = [
    "^Who is ",
    "^What is ",
    "^What was ",
    "^What does ",
    "^What Defines a ",
    ": The Complete Guide$",
    "Definition & Explanation$",
    "Explanation$",
    "Definition and Uses$",
    "Definition and Levels$",
    "Definition and Example$",
    "Definition and Tactics$",
    "Definition and Applications$",
    "Definition and Application$",
    "Definition and Trading Uses$",
    "Defining the$",
    "Defining an$",
    "Defining a$",
    "Defining$",
    "Defined$",
    "- Definition$",
    "– Definition$",
    "Definition",
    "Defintion",
    " in Finance$",
    " in Finance\?$",
    "^The ",
    "^An ",
    "^A ",
    "\?$",
]

COMPILED_REGEXES = [re.compile(p, re.IGNORECASE) for p in PATTERNS_TO_REMOVE]


def get_svo_output_path(path):
    """Return output_path that is destination for extracted SVO triples."""
    path = Path(path)
    output_path = path.with_name(f"{path.stem}-svo{path.suffix}")

    return output_path


def get_settings(output=None):
    """Call get_project_settings() to get settings from settings.py,
    complete FEED_URI_TEMPLATE and add FEED_URI (which is raw_path)
    to settings dict.

    Returns:
        settings: dict to configure crawling
    """
    raw_path = output or FEED_URI_TEMPLATE.format(
        filename=datetime.now().strftime("auto%Y-%m-%dT%H-%M-%S")
    )

    settings = get_project_settings()
    settings["FEED_URI"] = raw_path
    return settings


def get_clean_investopedia_title(title):
    """Return page title without unnecessary text."""

    for r in COMPILED_REGEXES:
        title = re.sub(r, "", title)

    return title.strip()


def get_term_names(data):
    """Return lowercase term names without brackets and their content."""
    return [get_clean_text(i["title"]) for i in data]


def get_clean_text(text):
    """Return lowercase text without brackets and their content."""
    text = text.replace("“", '"').replace("”", '"').lower()

    for r in [BRACKETS_REGEX, ABBR_REGEX]:
        text = re.sub(r, "", text)

    return text
