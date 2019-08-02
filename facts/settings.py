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

# test set of words to exclude from default stop words list
NOT_STOP_WORDS = ["is", "are", "be", "take", "make"]
