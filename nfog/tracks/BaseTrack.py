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
        """
        Get track title in it's simplest form.

        Returns None if title contains the Language, Codec, or Encoding Library.
        The track title should only be used for extra flag information, or as an
        actual track name.

        Examples:

        | Language | Track Title                   | Output                        |
        | -------- | ----------------------------- | ----------------------------- |
        | es       |                               |                               |
        | es       | Spanish                       |                               |
        | es       | Spanish (Latin American, SDH) |                               | ! info loss
        | es       |  (Latin American, SDH)        | (Latin American, SDH)         |
        | es       | Latin American (SDH)          | Latin American (SDH)          |
        | es       | Commentary by John & Jane Doe | Commentary by John & Jane Doe |
        | es       | AC-3                          |                               |
        | es       | DD                            |                               |
        | es       | AC3 2.0                       |                               |
        | es       | 2.0                           | 2.0 (too probable to happen)  |
        | es       | Stereo                        |                               |
        | es       | H.264                         |                               |
        | es       | H264                          |                               |
        | es       | x264                          |                               |
        """
        title = (self._x.title or "").strip()
        if not title:
            return None

        try:
            # checks by name only, instead of tag as tag can be triggered in non-tag
            # cases, like `SDH` as title, which is detected as Southern Kurdish
            if Language.find(title) != Language.get("und"):
                return None
        except LookupError:
            pass

        if any(str(x).lower() in title.lower() for x in (
            # Codec (e.g. E-AC-3, EAC3, H.264, H264, VC-1, VC1)
            self._x.format,
            self.ALPHA_NUMERIC_RE.sub("", self._x.format),
            # Simplified Codec (e.g., DD, DD+, DDP)
            self.codec,
            self.ALPHA_NUMERIC_RE.sub("", self.codec.replace("+", "P")),
            # Encoding library (if available)
            (self._x.writing_library or "").split(" ")[0],
            # Channel layout as generic name
            # Float representation not checked as too probable
            "Mono",
            "Stereo",
            "Surround",
            "Atmos"
        ) if x):
            return None

        return title


__ALL__ = (BaseTrack,)
