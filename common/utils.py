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
