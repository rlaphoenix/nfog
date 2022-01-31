from pathlib import Path

import toml
from appdirs import user_data_dir


class Directories:
    user_data = Path(user_data_dir("nfog", False))
    templates = user_data / "templates"
    artwork = user_data / "artwork"


class Files:
    config = Directories.user_data / "config.toml"
    template = Directories.templates / "{name}.nfo"


if Files.config.exists():
    config = toml.load(Files.config)
else:
    config = {}


__ALL__ = (config, Directories, Files)
