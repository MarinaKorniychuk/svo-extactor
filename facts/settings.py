# -*- coding: utf-8 -*-
from os import environ

"""Common settings and globals."""

# ===== SCRAPY =====

SPIDER_MODULES = ["facts.spiders"]

FEED_URI_TEMPLATE = "data/{source}/raw/{filename}"
FEED_FORMAT = "csv"

LOG_LEVEL = "INFO"


# ===== REQUESTS =====

HTTPCACHE_ENABLED = True
DOWNLOAD_DELAY = 0.2
RETRY_TIMES = 3


# ===== SPACY =====

TOKENS_TO_FILTER = ("PUNCT", "DET", "ADP", "SPACE", "PRON", "PROPN")


# ===== EXPORTING =====

# Destination settings
OUTPUT_FILE_TEMPLATE = "data/{source}/{filename}"

DEBUG = environ.get("DEBUG", False)
