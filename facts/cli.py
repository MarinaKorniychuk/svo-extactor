import logging

import click

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from common.utils import get_settings
from facts.handlers import CSVHandler
from facts.extractors import SVOExtractor

from . import __doc__


@click.group(help=__doc__)
def cli():
    pass


@cli.command()
@click.option(
    "--output_file",
    required=False,
    default=None,
    help="dump extracted items into OUTPUT FILE",
)
@click.option(
    "--data_file",
    required=False,
    default=None,
    help="read fetched items from DATA FILE instead of crawling from SOURCE",
)
@click.argument("source")
def extract(source, output_file, data_file):
    """Run spider to crawl data from specified SOURCE (that is spider's name)
    or simply read previously fetched data from specified DATA FILE,
    call SVO extractor to generate SVO triples and save them to OUTPUT FILE.
    """
    logger = logging.getLogger("facts")
    settings, raw_path, output_path = get_settings(source, output_file, data_file)

    if not data_file:
        # the reactor should be explicitly run and shut down after the crawling
        # is finished (by adding callbacks to the deferred)
        runner = CrawlerRunner(settings)
        deferred = runner.crawl(source)
        deferred.addBoth(lambda _: reactor.stop())

        logger.info(f"Starting spider: {source}")
        reactor.run()  # the script will block here until the crawling is finished

    handler = CSVHandler()
    extractor = SVOExtractor()

    # extracting svo triples
    fetched_data = handler.read_from_file(raw_path)
    svo_triples = extractor.process(fetched_data)

    # saving svo triples to file
    handler.export_to_file(svo_triples, output_path)


__all__ = ["cli"]
