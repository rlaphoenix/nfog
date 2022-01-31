import click

from nfog.constants import GROUP_SETTINGS


@click.group(context_settings=GROUP_SETTINGS)
def cli() -> None:
    """
    \b
    nfog
    Scriptable Database-Driven NFO Generator for Movies and TV.
    https://github.com/rlaphoenix/nfog
    """
