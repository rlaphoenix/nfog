from __future__ import annotations

from pathlib import Path

import pymediainfo

from nfog.tracks.BaseTrack import BaseTrack


class Subtitle(BaseTrack):
    def __init__(self, track: pymediainfo.Track, path: Path):
        super().__init__(track, path)

    @property
    def codec(self) -> str:
        """
        Get track codec in common P2P simplified form.
        E.g., 'SubRip (SRT)' instead of 'UTF-8'.
        """
        return {
            "UTF-8": "SubRip (SRT)",
        }.get(self._x.format, self._x.format)


__ALL__ = (Subtitle,)
