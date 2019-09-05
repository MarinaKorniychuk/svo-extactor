import logging

import click

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from common.utils import get_settings, get_svo_output_path
from facts.handlers import CSVHandler
from facts.extractors import SVOExtractor

from . import __doc__


@click.group(help=__doc__)
def cli():
    pass


@cli.command()
@click.option("--output", "-o", metavar="FILE", help="dump scraped items into FILE")
@click.argument("source")
def crawl(source, output):
    """Run spider to crawl data from specified SOURCE (spider's name)"""
    logger = logging.getLogger("facts")
    settings = get_settings(output)

    runner = CrawlerRunner(settings)
    deferred = runner.crawl(source)
    deferred.addBoth(lambda _: reactor.stop())

    logger.info(f"Starting spider: {source}")
    reactor.run()  # the script will block here until the crawling is finished

    logger.info("Spider closed (finished)")


@cli.command()
@click.argument("raw_path")
def extract(raw_path):
    """Read previously fetched data from RAW_PATH,
    call SVO extractor to generate SVO triples and export them to CSV file.
    """
    logger = logging.getLogger("facts")
    output_path = get_svo_output_path(raw_path)

    handler = CSVHandler()
    fetched_data = handler.read_from_file(raw_path)

    extractor = SVOExtractor()
    logger.info(f"Starting extracting SVO from: {raw_path}")
    svo_triples = extractor.process(fetched_data)

    handler.export_to_file(svo_triples, output_path)


__all__ = ["cli"]
