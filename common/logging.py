import json
import pathlib
import logging.config

from facts.settings import DEBUG


def setup_logging():
    with open(
        pathlib.Path.joinpath(pathlib.Path(__file__).parent, "logging.json")
    ) as f:
        logging_config = json.load(f)

    if DEBUG:
        for logger_name, logger_info in logging_config["loggers"].items():
            logger_info["level"] = "DEBUG"

    logging.config.dictConfig(logging_config)
