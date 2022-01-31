from __future__ import annotations

import gzip
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import click
import jsonpickle
import toml
from click_default_group import DefaultGroup
from pymediainfo import MediaInfo

from nfog import __version__
from nfog.artwork import Artwork
from nfog.config import Directories, Files, config
from nfog.constants import GROUP_SETTINGS
from nfog.templates import Template
from nfog.templates.Group import TemplateGroup


@click.group(
    cls=DefaultGroup,
    default="generate",
    default_if_no_args=True,
    context_settings=GROUP_SETTINGS
)
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
        "https://github.com/rlaphoenix/nfog\n"
        "\n"
        f"Configuration File: {Files.config}\n"
        f"Templates Folder: {Directories.templates}\n"
        f"Artwork Folder: {Directories.artwork}"
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
        fn = Files.artwork(artwork)
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

    out_path: Path = file.parent / f"{template.release_name}{template.file_ext}"
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


@cli.command()
@click.argument("out_dir", type=Path)
def export(out_dir: Path) -> None:
    """Export all configuration, artwork, and templates."""
    if not out_dir or not out_dir.is_dir():
        raise click.ClickException("Save Path must be directory.")
    art = {x.stem: x.read_text(encoding="utf8") for x in Directories.artwork.glob("*.py")}
    tmpl = {x.stem: x.read_text(encoding="utf8") for x in Directories.templates.glob("*.py")}
    json = jsonpickle.dumps({
        "version": 1,
        "config": config,
        "artwork": art,
        "templates": tmpl
    })
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"pynfogen.export.{datetime.now().strftime('%Y%m%d-%H%M%S')}.json.gz"
    out_path.write_bytes(gzip.compress(json.encode("utf8")))
    print(f"Successfully exported to: {out_path}")


@cli.command(name="import")
@click.argument("file", type=Path)
def import_(file: Path):
    """
    Import all configuration, artwork, and templates from export.
    The configuration will be overwritten in it's entirety.
    Current artwork and template files will only be overwritten if
    they have the same name.
    """
    if not file or not file.exists():
        raise click.ClickException("File path does not exist.")
    decompress = gzip.open(file).read().decode("utf8")
    json = jsonpickle.decode(decompress)
    Files.config.parent.mkdir(parents=True, exist_ok=True)
    Directories.artwork.mkdir(parents=True, exist_ok=True)
    Directories.templates.mkdir(parents=True, exist_ok=True)
    Files.config.write_text(toml.dumps(json["config"]))
    print("Imported Configuration")
    for name, data in json["artwork"].items():
        path = (Directories.artwork / name).with_suffix(".py")
        path.write_text(data, encoding="utf8")
        print(f"Imported Artwork: {name}")
    for name, data in json["templates"].items():
        path = (Directories.templates / name).with_suffix(".py")
        path.write_text(data, encoding="utf8")
        print(f"Imported Template: {name}")
    print(f"Successfully Imported from {file}!")
