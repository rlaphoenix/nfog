from pathlib import Path

import toml
from appdirs import user_data_dir


class Directories:
    user_data = Path(user_data_dir("nfog", False))
    templates = user_data / "templates"
    artwork = user_data / "artwork"


class Files:
    config = Directories.user_data / "config.toml"
    template = lambda name: Directories.templates / f"{name}.py"  # noqa: E731
    artwork = lambda name: Directories.artwork / f"{name}.py"  # noqa: E731


if Files.config.exists():
    config = toml.load(Files.config)
else:
    config = {}


__ALL__ = (config, Directories, Files)
