# nfog

[![License](https://img.shields.io/github/license/rlaphoenix/nfog)](https://github.com/rlaphoenix/nfog/blob/master/LICENSE)
[![Python Support](https://img.shields.io/pypi/pyversions/nfog)](https://pypi.python.org/pypi/nfog)
[![Release](https://img.shields.io/pypi/v/nfog)](https://pypi.python.org/pypi/nfog)
[![GitHub issues](https://img.shields.io/github/issues/rlaphoenix/nfog)](https://github.com/rlaphoenix/nfog/issues)

Scriptable Database-Driven NFO Generator for Movies and TV.

## Installation

    pip install --user nfog

## Building

### Dependencies

- [Python](https://python.org/downloads) (v3.7 or newer)
- [Poetry](https://python-poetry.org/docs) (latest recommended)

### Installation

1. `git clone https://github.com/rlaphoenix/nfog`
2. `cd nfog`
3. `poetry config virtualenvs.in-project true` (optional, but recommended)
4. `poetry install`
5. `nfo -h`

## Creating Templates

We use Template's to define the structure and logic that creates your NFO file. Your Template file may
create NFOs of any kind of encoding or style, including ASCII, ANSI, and such. You don't have to conform
to any specifications of any kind, but are encouraged to if possible.

To create a Template file, you simply need to inherit the `Template` class in `nfog.template`, fill out
the various abstract methods/properties, and create an `nfo` property that returns a final string.

Take a look at the [Example Templates](/examples/templates) for pre-made examples for various NFO
usage scenarios. You may modify these Templates in any way you like.

Note: While you have complete freedom with what Python code you run from within the template, this also
means you should not immediately trust template file as they are after all still Python files.

## Creating Artwork

Just like Templates, we use Artwork files to define the look and style of the surrounding NFO.
You may also do introspection of the NFO output to merge style within the contents of the NFO as well.

To create an Artwork file, inherit the `Artwork` class in `nfog.artwork`, fill out any abstract methods
and properties, and create the `with_template` function that returns the final string containing both
the NFO output (from `template` argument) and the Artwork.

Take a look at the [Example Artwork](/examples/artwork) to see how these are used. However, you cannot
re-use these, or make derivative works. Please see the [Artwork License](/examples/artwork/LICENSE)
for more information.

## Using Templates and Artwork

To use Templates and Artwork, calling `nfo` (or `nfo generate`) will ask you for various information, but
one of them is a Template to use. The Templates it makes available to use are loaded from the user templates
directory which can be found by typing `nfo version`.

To use an Artwork, specify the name of the Artwork file (case-sensitive) to `-a/--artwork`.
Using an Artwork is completely optional.

For more information on using `nfog`, see the usage help by calling `nfo --help`.

## License

[Apache License, Version 2.0](LICENSE)
