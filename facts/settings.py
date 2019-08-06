"""Common settings and globals."""

# Scrapy Settings
SPIDER_MODULES = ["facts.spiders"]
FEED_URI_TEMPLATE = "data/{source}/raw/{filename}"
FEED_FORMAT = "csv"

HTTPCACHE_ENABLED = True
RETRY_TIMES = 3

LOG_LEVEL = "INFO"

# Destination settings
OUTPUT_FILE_TEMPLATE = "data/{source}/{filename}"

# nlp settings

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
