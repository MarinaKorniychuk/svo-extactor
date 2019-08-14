import logging

import click

from scrapy.crawler import CrawlerProcess

from common.logging import setup_logging
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
@click.argument("source")
def extract(output_file, source):
    """Run spider to crawl data from specified SOURCE (that is spider's name),
    call SVO extractor to generate SVO triples and save them to OUTPUT FILE.
    """
    settings, raw_path, output_path = get_settings(source, output_file)

    logger = logging.getLogger("facts")
    logger.info(f"Starting spider: {source}")
    process = CrawlerProcess(settings, install_root_handler=False)
    setup_logging()
    process.crawl(source)
    process.start()

    handler = CSVHandler()
    extractor = SVOExtractor()

    # extracting svo triples
    fetched_data = handler.read_from_file(raw_path)
    svo_triples = extractor.process(fetched_data)

    # saving svo triples to file
    handler.export_to_file(svo_triples, output_path)


__all__ = ["cli"]
