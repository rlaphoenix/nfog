from pathlib import Path

import toml
from appdirs import user_data_dir


class Directories:
    user_data = Path(user_data_dir("pynfogen", False))


class Files:
    config = Directories.user_data / "config.toml"


if Files.config.exists():
    config = toml.load(Files.config)
else:
    config = {}


__ALL__ = (config, Directories, Files)
