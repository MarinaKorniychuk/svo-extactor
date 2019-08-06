from datetime import datetime

import click

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from facts.settings import FEED_URI_TEMPLATE, OUTPUT_FILE_TEMPLATE

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
    output_file = output_file or datetime.now().strftime("auto%Y-%m-%dT%H:%M:%S.csv")

    raw_path = FEED_URI_TEMPLATE.format(source=source, filename=output_file)
    output_path = OUTPUT_FILE_TEMPLATE.format(source=source, filename=output_file)

    # fetching data from dictionary and saving to output file
    settings = get_project_settings()
    settings["FEED_URI"] = raw_path
    process = CrawlerProcess(settings)
    process.crawl(source)
    process.start()

    # extracting svo triples
    pass

    # saving svo triples to file
    pass


__all__ = ["cli"]
