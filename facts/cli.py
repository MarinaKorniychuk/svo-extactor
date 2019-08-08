import csv

import click

from scrapy.crawler import CrawlerProcess

from common.utils import get_settings
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
    settings, raw_path, output_path = get_settings(output_file, source)


    # fetching data from dictionary and saving to output file
    process = CrawlerProcess(settings)
    process.crawl(source)
    process.start()

    # extracting svo triples
    fetched_data = [item for item in csv.DictReader(open(raw_path))]
    svo_handler = SVOExtractor()
    svo_triples = svo_handler.process(fetched_data)

    # saving svo triples to file
    pass


__all__ = ["cli"]
