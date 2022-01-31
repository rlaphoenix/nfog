from __future__ import annotations

import re
import textwrap
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

    @staticmethod
    def indented_wrap(text: str, width: int, indent: Optional[str] = None, **kwargs) -> str:
        """
        Wrap text at a specific width and indent.
        The `indent` value will set an initial and subsequent indent. If
        set, it will override any indent options you may have also provided via kwargs.
        """
        if not text:
            return text
        if not width or width < 1:
            raise ValueError(f"An invalid width value of [{width}] was provided.")
        if indent:
            kwargs["initial_indent"] = indent
            kwargs["subsequent_indent"] = indent
        return "\n".join(textwrap.wrap(text, width, **kwargs))

    @staticmethod
    def centered_wrap(text: str, width: int, wrap_width: Optional[int] = None) -> str:
        """
        Center text to a specific width, while also wrapping at another width.
        If wrap_width is not provided, width will be used instead.
        """
        if not text:
            return text
        if not width or width < 1:
            raise ValueError(f"An invalid width value of [{width}] was provided.")
        if wrap_width and wrap_width < width:
            raise ValueError(f"Wrap width [{wrap_width}] cannot be less than centering width [{width}].")
        return "\n".join([
            x.center(width)
            for x in textwrap.wrap(text, wrap_width or width)
        ])


__ALL__ = (Template,)
