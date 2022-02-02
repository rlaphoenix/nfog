from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

import pymediainfo
from langcodes import Language


class BaseTrack:
    ALPHA_NUMERIC_RE = re.compile(r"[\W]+")

    """Track to aide in overriding properties of a PyMediaInfo Track instance."""
    def __init__(self, track: pymediainfo.Track, path: Path):
        self._x = track
        self._path = path
        # common shorthands
        self.bitrate = self._x.other_bit_rate[0]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._x, name)

    @property
    def all_properties(self) -> defaultdict[str, Any]:
        """Get all non-callable attributes from this and it's sub-track object."""
        props = defaultdict(lambda: None)

        for obj in (self, self._x):
            for k, v in obj.__dict__.items():
                if k in ("_x", "_path"):
                    continue
                props[k] = v

        for subclass in (BaseTrack, self.__class__):
            for k, v in vars(subclass).items():
                if not isinstance(v, property):
                    continue
                if k in ("all_properties",):
                    continue
                props[k] = getattr(self, k)

        return props

    @property
    def language(self) -> Optional[Language]:
        """
        Return track language as a Language object.
        Returns None if no language is specified, or if set to `und`.
        """
        if self._x.language and self._x.language != "und":
            return Language.get(self._x.language)
        return None

    @property
    def title(self) -> Optional[str]:
        """Get track title in it's simplest form."""
        return (self._x.title or "").strip() or None


__ALL__ = (BaseTrack,)
