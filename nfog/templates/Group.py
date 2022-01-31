from typing import Any, Optional

import click

from nfog.config import Directories


class TemplateGroup(click.MultiCommand):
    """Lazy-loaded command group of nfo templates."""
    TEMPLATES_DIR = Directories.templates

    def list_commands(self, ctx: click.Context) -> list[str]:
        """Returns a list of template names from the template filenames."""
        rv = []
        if self.TEMPLATES_DIR.is_dir():
            for cmd in self.TEMPLATES_DIR.iterdir():
                if cmd.stem.lower() not in ("__init__", "group") and cmd.suffix.lower() == ".py":
                    rv.append(cmd.stem)
        if not rv:
            raise click.ClickException(f"No Templates were found in {Directories.templates}")
        rv.sort()
        return rv

    def get_command(self, ctx: click.Context, name: str) -> Optional[click.Command]:
        """Load the template code and return the main click command function."""
        scope: dict[str, Any] = {}
        fn = self.TEMPLATES_DIR / f"{name}.py"
        if not fn.exists():
            raise click.ClickException(f"The Template ({name}) was not found in {Directories.templates}.")
        with fn.open(encoding="utf8") as f:
            code = compile(f.read(), fn, "exec")
            eval(code, scope, scope)
        return scope[name].cli
