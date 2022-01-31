from __future__ import annotations

import re
from abc import abstractmethod
from pathlib import Path
from typing import Optional, Any

from imdb import IMDb
from pymediainfo import MediaInfo, Track
from requests import Session


class Template:
    IMDB_ID_T = re.compile(r"^tt\d{7,8}$")
    TMDB_ID_T = re.compile(r"^(tv|movie)/\d+$")
    TVDB_ID_T = re.compile(r"^\d+$")

    def __init__(
        self,
        file: Path,
        imdb: str,
        tmdb: Optional[str] = None,
        tvdb: Optional[int] = None,
        source: Optional[str] = None,
        note: Optional[str] = None,
        preview: Optional[str] = None,
        **kwargs: Any
    ):
        self._nfo = []

        self.file = file

        if not imdb:
            raise ValueError("An IMDb ID is required, but was not provided.")
        if not self.IMDB_ID_T.match(imdb):
            raise ValueError(
                f"The provided IMDb ID ({imdb}) is not valid. Expected e.g., 'tt0487831', 'tt10810424'."
            )
        if tmdb and not self.TMDB_ID_T.match(tmdb):
            raise ValueError(
                f"The provided TMDB ID ({tmdb}) is not valid. Expected e.g., 'tv/2490', 'movie/14836'."
            )
        if tvdb and not self.TVDB_ID_T.match(str(tvdb)):
            raise ValueError(
                f"The provided TVDB ID ({tvdb}) is not valid. Expected e.g., '79216', '1395'."
            )

        self.imdb = IMDb().get_movie(imdb.lstrip("tt"), ("main", "episodes"))
        self.tmdb = tmdb
        self.tvdb = tvdb
        self.source = source
        self.note = note
        self.preview = preview
        self.args = kwargs

        self.media_info = MediaInfo.parse(self.file)
        self.video_tracks = self.media_info.video_tracks
        self.audio_tracks = self.media_info.audio_tracks
        self.text_tracks = self.media_info.text_tracks

        self.chapters: Optional[Track] = next(iter(self.media_info.menu_tracks), None)
        if self.chapters:
            self.chapters = {
                ".".join([k.replace("_", ".")[:-3], k[-3:]]): v.strip(":")
                for k, v in self.chapters.to_data().items()
                if f"1{k.replace('_', '')}".isdigit()
            }

        self.primary_lang = next(
            (
                lang.language
                for lang in sorted(self.audio_tracks, key=lambda x: x.streamorder)
                if lang.language
            ),
            # default to first language on IMDb
            self.imdb["language codes"][0]
        )

        self._session = None

    @property
    @abstractmethod
    def nfo(self) -> str:
        """Generate the NFO string using Template information."""

    @property
    @abstractmethod
    def release_name(self) -> str:
        """The release name used for the output NFO filename."""

    @property
    def session(self) -> Session:
        """Get a Request Session."""
        if self._session is not None:
            return self._session

        self._session = Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
            "Accept-Language": "en-US,en;q=0.5"
        })

        return self._session


__ALL__ = (Template,)
