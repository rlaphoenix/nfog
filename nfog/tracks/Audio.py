from __future__ import annotations

from pathlib import Path

import pymediainfo

from nfog.tracks.BaseTrack import BaseTrack


class Audio(BaseTrack):
    AUDIO_CHANNEL_LAYOUT_WEIGHT = {
        "LFE": 0.1
    }

    def __init__(self, track: pymediainfo.Track, path: Path):
        super().__init__(track, path)

    @property
    def codec(self) -> str:
        """
        Get track codec in common P2P simplified form.
        E.g., 'DD+' instead of 'E-AC-3'.
        """
        return {
            "E-AC-3": "DD+",
            "AC-3": "DD"
        }.get(self._x.format, self._x.format)

    @property
    def channels(self) -> float:
        """Get track channels as channel layout representation."""
        if self._x.channel_layout:
            return float(sum(
                self.AUDIO_CHANNEL_LAYOUT_WEIGHT.get(x, 1)
                for x in self._x.channel_layout.split(" ")
            ))
        return float(self._x.channel_s)


__ALL__ = (Audio,)
