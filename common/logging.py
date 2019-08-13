import json
import pathlib
import logging.config

from facts.settings import DEBUG


def setup_logging():
    """Load logging.json config and set specified logging settings.

    Note:
        Need to be called after initializing scrapy CrawlerProcess with
        install_root_handler=False to get logging from scrapy build-in
        loggers with useful logs (stats and crawling errors).
    """
    with open(
        pathlib.Path.joinpath(pathlib.Path(__file__).parent, "logging.json")
    ) as f:
        logging_config = json.load(f)

    if DEBUG:
        for logger_name, logger_info in logging_config["loggers"].items():
            logger_info["level"] = "DEBUG"

    logging.config.dictConfig(logging_config)
