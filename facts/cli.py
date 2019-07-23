import click

from . import __doc__


@click.group(help=__doc__)
def cli():
    pass


__all__ = ["cli"]
