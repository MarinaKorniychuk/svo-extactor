import re
from datetime import datetime
from pathlib import Path

from scrapy.utils.project import get_project_settings

from facts.settings import FEED_URI_TEMPLATE


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


def get_clear_title(title):
    """Return page title without unnecessary text."""
    patterns = [
        (r"^Who is ", ""),
        (r"^What is ", ""),
        (r"^What was ", ""),
        (r"^What does ", ""),
        (r"^What Defines a  ", ""),
        (r"Definition and Uses$", ""),
        (r"Definition and Levels$", ""),
        (r"Definition and Example$", ""),
        (r"Definition and Tactics$", ""),
        (r"Definition and Applications$", ""),
        (r"Definition and Application$", ""),
        (r"Definition and Trading Uses$", ""),
        (r"Defining the$", ""),
        (r"Defining an$", ""),
        (r"Defining a$", ""),
        (r"Defining$", ""),
        (r"Defined$", ""),
        (r"- Definition$", ""),
        (r"– Definition$", ""),
        (r"Definition", ""),
        (r" in Finance$", ""),
        (r"^The ", ""),
        (r"^An ", ""),
        (r"^A ", ""),
        (r"\?$", ""),
    ]

    for p in patterns:
        if re.findall(p[0], title, flags=re.IGNORECASE):
            title = re.sub(p[0], p[1], title, flags=re.IGNORECASE)

    return title.strip()
