import logging
from typing import Optional

import click
import toml

from nfog import __version__
from nfog.config import Files, config
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


@click.command(name="config")
@click.argument("key", type=str, required=False)
@click.argument("value", type=str, required=False)
@click.option("--unset", is_flag=True, default=False, help="Unset/remove the configuration value.")
def config_(key: Optional[str], value: Optional[str], unset: bool) -> None:
    """Manage or view user configuration data."""
    if not key and not value:
        print(toml.dumps(config).rstrip())
        return

    log = logging.getLogger("config")

    tree = key.split(".")
    temp = config
    for t in tree[:-1]:
        if temp.get(t) is None:
            temp[t] = {}
        temp = temp[t]

    if unset:
        if tree[-1] in temp:
            del temp[tree[-1]]
        log.info(f"Unset {key}")
    else:
        if value is None:
            if tree[-1] not in temp:
                raise click.ClickException(f"Key {key} does not exist in the config.")
            print(f"{key}: {temp[tree[-1]]}")
        else:
            temp[tree[-1]] = value
            log.info(f"Set {key} to {repr(value)}")
            Files.config.parent.mkdir(parents=True, exist_ok=True)
            toml.dump(config, Files.config)
