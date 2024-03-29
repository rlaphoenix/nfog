from __future__ import annotations

import re
import textwrap
from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import tmdbsimple
from imdb import Cinemagoer
from langcodes import closest_supported_match
from pymediainfo import MediaInfo, Track
from requests import Session

from nfog.config import config
from nfog.parsers.imdb import IMDb
from nfog.tracks import Audio, Subtitle, Video


class Template:
    IMDB_ID_T = re.compile(r"^tt\d{7,8}$")
    TMDB_ID_T = re.compile(r"^(tv|movie)/\d+$")
    TVDB_ID_T = re.compile(r"^\d+$")

    def __init__(
        self,
        file: Path,
        imdb: Optional[str],
        tmdb: Optional[str] = None,
        tvdb: Optional[int] = None,
        source: Optional[str] = None,
        note: Optional[str] = None,
        preview: Optional[str] = None,
        **kwargs: Any
    ):
        self._nfo = []

        self.file = file

        if imdb:
            if not self.IMDB_ID_T.match(imdb):
                raise ValueError(
                    f"The provided IMDb ID ({imdb}) is not valid. Expected e.g., 'tt0487831', 'tt10810424'."
                )

            self._cinemagoer = Cinemagoer()
            self.imdb = self._cinemagoer.get_movie(imdb.lstrip("tt"))
            if "movie" not in self.imdb["kind"]:
                # broken, very manual fix below
                # self._cinemagoer.update(self.imdb, ("episodes",))
                imdb_object = IMDb(imdb.lstrip("tt"))
                self.imdb["episodes"] = {}
                for season in range(1, self.imdb["seasons"] + 1):
                    self.imdb["episodes"][season] = imdb_object.get_episodes(int(season))
        else:
            self.imdb = None

        if tmdb:
            if not self.TMDB_ID_T.match(tmdb):
                raise ValueError(
                    f"The provided TMDB ID ({tmdb}) is not valid. Expected e.g., 'tv/2490', 'movie/14836'."
                )
            if not tmdbsimple.API_KEY:
                raise EnvironmentError("No themoviedb.org api key in config, cannot proceed.")
            self.tmdb = {
                "movie": tmdbsimple.Movies,
                "tv": tmdbsimple.TV
            }[tmdb.split("/")[0]](tmdb.split("/")[1])
        else:
            self.tmdb = None

        if tvdb:
            if not self.TVDB_ID_T.match(str(tvdb)):
                raise ValueError(
                    f"The provided TVDB ID ({tvdb}) is not valid. Expected e.g., '79216', '1395'."
                )
            # tvdb api isn't free, harder to implement
            self.tvdb = tvdb
        else:
            self.tvdb = None

        self.source = source
        self.note = note
        self.preview = preview
        self.args = kwargs

        self.media_info = MediaInfo.parse(self.file)
        self.video_tracks = [Video(x, self.file) for x in self.media_info.video_tracks]
        self.audio_tracks = [Audio(x, self.file) for x in self.media_info.audio_tracks]
        self.text_tracks = [Subtitle(x, self.file) for x in self.media_info.text_tracks]

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
            self.imdb["language codes"][0] if self.imdb else None
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
    @abstractmethod
    def file_ext(self) -> str:
        """The file extension to use when saving this template."""

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

    def get_preview_images(self, url: str) -> list[tuple[str, str]]:
        """Get a list of image thumbnail SRCs and full hyperlinks from Gallery url."""
        if not url:
            raise ValueError("Provided URL cannot be empty.")

        domain = ".".join(urlparse(url).netloc.split(".")[-2:])
        supported_domains = ["imgbox.com", "beyondhd.co"]
        if domain not in supported_domains:
            return []

        images = []
        page = self.session.get(url).text
        if domain == "imgbox.com":
            for m in re.finditer(r'src="(https://thumbs2.imgbox.com.+/)(\w+)_b.([^"]+)', page):
                images.append((
                    f"https://imgbox.com/{m.group(2)}",
                    f"{m.group(1)}{m.group(2)}_t.{m.group(3)}"
                ))
        if domain == "beyondhd.co":
            for m in re.finditer(r'/image/([^"]+)"\D+src="(https://.*beyondhd.co/images.+/(\w+).md.[^"]+)', page):
                images.append((
                    f"https://beyondhd.co/image/{m.group(1)}",
                    m.group(2)
                ))

        return images

    def get_banner_image(self, tvdb_id: int, language: str) -> Optional[str]:
        """Get a wide banner image from fanart.tv."""
        if not tvdb_id:
            return None

        api_key = config.get("api-keys", {}).get("fanart-tv")
        if not api_key:
            print("Warning: No fanart.tv api key in config, skipping banner image.")
            return None

        r = self.session.get(f"http://webservice.fanart.tv/v3/tv/{tvdb_id}?api_key={api_key}")
        if r.status_code == 404:
            return None
        res = r.json()

        error = res.get("error message")
        if error:
            if error == "Not found":
                return None
            raise ValueError(f"An unexpected error occurred while calling Fanart.tv, {res}")

        url = next((
            x["url"]
            for x in res.get("tvbanner") or []
            if closest_supported_match(x["lang"], [language], 5)
        ), None)

        return url

    def get_video_summary(self, video: Video) -> str:
        """Get a video track's information in a two-line summary."""
        line_1 = "- "
        if video.language:
            line_1 += f"{video.language.display_name(self.primary_lang)}, "

        line_1 += f"{video.codec} ({video.profile}) "
        line_1 += f"{video.width}x{video.height} ({video.dar}) "
        line_1 += f"@ {video.bitrate}"
        if video.bit_rate_mode:
            line_1 += f" ({video.bit_rate_mode})"

        line_2 = f"  {video.fps} FPS "
        line_2 += f"({video.frame_rate_mode}), "
        line_2 += f"{video.color_space} {video.chroma_subsampling} {video.bit_depth}bps, "
        line_2 += f"{video.range}, {video.scan}"

        return "\n".join([line_1, line_2])

    def get_audio_summary(self, audio: Audio) -> str:
        """Get an audio track's information in a one-line summary."""
        line = "- "
        if audio.language:
            line += f"{audio.language.display_name(self.primary_lang)}, "

        if audio.title:
            line += f"{audio.title}, "
        line += f"{audio.codec} {audio.channels} "
        line += f"@ {audio.bitrate}"
        if audio.bit_rate_mode:
            line += f" ({audio.bit_rate_mode})"

        return line

    def get_subtitle_summary(self, subtitle: Subtitle) -> str:
        """Get a subtitle track's information in a one-line summary."""
        line = "- "
        if subtitle.language:
            line += f"{subtitle.language.display_name(self.primary_lang)}, "

        if subtitle.title:
            line += f"{subtitle.title}, "
        line += subtitle.codec

        return line

    @staticmethod
    def get_chapter_list(chapters: Optional[dict[str, str]]) -> list[str]:
        """Get a list of chapters showing timecode and chapter name."""
        if not chapters:
            return []
        return [
            f"- {k}: {v}"
            for k, v in chapters.items()
        ]

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
            x.center(width).rstrip()
            for x in textwrap.wrap(text, wrap_width or width)
        ])

    @staticmethod
    def layout(items: list[str], width: int, spacing: int = 0) -> str:
        """
        Lay out data in a grid with specific widths and spacing.

        Example:
            >>> Template.layout(['1', '2', '3'], width=2)
            12
            3
            >>> Template.layout(['1', '2', '3', '4', '5', '6', '7'], width=4)
            1234
            567
            >>> Template.layout(['1', '2', '3', '4'], width=2, spacing=1)
            1 2

            3 4
        """
        if not items:
            return ""

        grid = [
            items[i:i + width]
            for i in range(0, len(items), width)
        ]

        grid_x_spaced = [(" " * spacing).join(x) for x in grid]
        grid_y_spaced = ("\n" * (spacing + 1)).join(grid_x_spaced)

        return grid_y_spaced


__ALL__ = (Template,)
