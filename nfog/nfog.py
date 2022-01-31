import click

from nfog import __version__
from nfog.constants import GROUP_SETTINGS


@click.group(context_settings=GROUP_SETTINGS)
def cli() -> None:
    """
    \b
    nfog
    Scriptable Database-Driven NFO Generator for Movies and TV.
    https://github.com/rlaphoenix/nfog
    """


@cli.command()
def version() -> None:
    """Shows the version of the project."""
    print(
        f"nfog {__version__}\n"
        f"Scriptable Database-Driven NFO Generator for Movies and TV.\n"
        "https://github.com/rlaphoenix/nfog"
    )
