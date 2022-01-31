from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

import click
import toml
from pymediainfo import MediaInfo

from nfog import __version__
from nfog.artwork import Artwork
from nfog.config import Directories, Files, config
from nfog.constants import GROUP_SETTINGS
from nfog.templates import Template
from nfog.templates.Group import TemplateGroup


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


@cli.group(cls=TemplateGroup, context_settings=dict(**GROUP_SETTINGS, ignore_unknown_options=True))
@click.argument("file", type=Path)
@click.argument("imdb", type=str)
@click.option("-tmdb", type=str, default=None, help="TMDB ID (including 'tv/' or 'movie/').")
@click.option("-tvdb", type=int, default=None, help="TVDB ID ('73244' not 'the-office-us').")
@click.option("-a", "--artwork", type=str, default=None, help="Artwork to use.")
@click.option("-s", "--source", type=str, default=None, help="Source information.")
@click.option("-n", "--note", type=str, default=None, help="Notes/special information.")
@click.option("-p", "--preview", type=str, default=None, help="Preview information, typically an URL.")
@click.option("-e", "--encoding", type=str, default="utf8", help="Text-encoding for output, input is always UTF-8.")
@click.pass_context
def generate(ctx: click.Context, file: Path, imdb: str, tmdb: str, tvdb: int, **__) -> None:
    """
    Generates an NFO for the provided file.

    \b
    The file provided should best represent the majority of the release.
    E.g., If Episode 1 and 2 has a fault not found on Episodes 3 onwards, then provide Episode 3.
    """
    if not file.exists():
        raise click.ClickException(f"The provided path ({file}) does not exist.")
    if not file.is_file():
        raise click.ClickException(f"The provided path ({file}) is not to a file.")

    media_info = MediaInfo.parse(file)

    if imdb == "-":
        imdb = media_info.general_tracks[0].to_data().get("imdb")
        if not imdb:
            raise ValueError("No IMDb ID was found within the file's metadata.")
        ctx.params["imdb"] = imdb

    if not tmdb:
        tmdb = media_info.general_tracks[0].to_data().get("tmdb")
        ctx.params["tmdb"] = tmdb

    if not tvdb:
        tvdb = media_info.general_tracks[0].to_data().get("tvdb")
        ctx.params["tvdb"] = tvdb


@generate.result_callback()
def generator(
    template: Template,
    file: Path,
    artwork: Optional[str] = None,
    encoding: str = "utf8",
    **__
) -> None:
    if artwork:
        fn = Directories.artwork / f"{artwork}.py"
        if not fn.exists():
            raise click.ClickException(f"Artwork ({fn}) does not exist.")
        scope: dict[str, Any] = {}
        with fn.open(encoding="utf8") as f:
            code = compile(f.read(), fn, "exec")
            eval(code, scope, scope)
        artwork: Artwork = scope[artwork]
        nfo = artwork.with_template(template)
    else:
        nfo = template.nfo

    out_path: Path = file.parent / f"{template.release_name}.nfo"
    out_path.write_text(nfo, encoding=encoding)
    print(f"Generated NFO for {template.release_name}")
    print(f" + Saved to: {out_path}")


@cli.command(name="config")
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
