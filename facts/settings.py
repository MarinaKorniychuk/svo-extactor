# -*- coding: utf-8 -*-
from os import environ

"""Common settings and globals."""

# ===== SCRAPY =====

SPIDER_MODULES = ["facts.spiders"]

FEED_URI_TEMPLATE = "data/{filename}.csv"
FEED_FORMAT = "csv"

LOG_LEVEL = "INFO"


# ===== REQUESTS =====

DOWNLOAD_DELAY = 0.2
RETRY_TIMES = 3


DEBUG = environ.get("DEBUG", False)
