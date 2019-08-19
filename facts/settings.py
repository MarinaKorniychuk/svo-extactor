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

# words to exclude from default spacy stop words list
NOT_STOP_WORDS = [
    "had",
    "two",
    "doing",
    "name",
    "have",
    "say",
    "becoming",
    "amount",
    "fifty",
    "keep",
    "side",
    "go",
    "show",
    "five",
    "seeming",
    "take",
    "seems",
    "seem",
    "done",
    "put",
    "fifteen",
    "are",
    "is",
    "forty",
    "will",
    "do",
    "make",
    "six",
    "were",
    "did",
    "sixty",
    "be",
    "does",
    "no",
    "becomes",
    "used",
    "nine",
    "could",
    "call",
    "was",
    "has",
    "being",
    "become",
    "been",
    "get",
    "give",
    "not",
]

TOKENS_TO_FILTER = ("PUNCT", "DET", "ADP", "SPACE", "PRON", "PROPN")


# ===== EXPORTING =====

# Destination settings
OUTPUT_FILE_TEMPLATE = "data/{source}/{filename}"

DEBUG = environ.get("DEBUG", False)
