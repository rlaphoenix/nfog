from __future__ import annotations

from typing import Any

import click

from nfog.templates import Template


class Episode(Template):
    """
    Template for single TV Episode files.
    The release name will be the provided file's name.

    Note:
    - This uses IMDb for Title information which might not match TMDB or TVDB.
    - IMDb commonly has multi-segment episodes as one episode, e.g. S01E01E02 as just
      one episode, unlike what is typically done on TMDB and TVDB.
    """

    @staticmethod
    @click.command(name="Episode")
    @click.argument("season", type=int)
    @click.argument("episode", type=int)
    @click.pass_context
    def cli(ctx: click.Context, **kwargs: Any) -> Template:
        return Episode(**ctx.parent.params, **kwargs)

    @property
    def nfo(self) -> str:
        """Generate the NFO string using Template information."""
        if self._nfo:
            return self._nfo

        season: int = self.args["season"]
        episode: int = self.args["episode"]
        episode_name: str = self.imdb["episodes"][season][episode]["title"]

        title = self.imdb["title"]
        type_ = self.imdb["kind"].title().replace("Tv", "TV")
        year = self.imdb["series years"]
        has_chapters = ["No", "Yes"][bool(self.chapters)]

        self._nfo.extend([
            self.indented_wrap(self.release_name, 66, "  "),
            "",
            f"  Title    : {title}",
            f"  Type     : {type_} ({year})",
            f"  Episode  : {season}x{episode} \"{episode_name}\"",
            f"  IMDb     : https://imdb.com/title/tt{self.imdb.movieID}"
        ])

        if self.tmdb:
            self._nfo.append(f"  TMDB     : https://themoviedb.org/{self.tmdb}")

        if self.tvdb:
            self._nfo.append(f"  TVDB     : https://thetvdb.com/?tab=series&id={self.tvdb}")

        self._nfo.extend([
            f"  Preview  : {self.preview}",
            f"  Chapters : {has_chapters}"
        ])

        if self.source:
            self._nfo.extend([
                "",
                "  Source :",
                self.indented_wrap(self.source, 66, "  ")
            ])

        if self.note:
            self._nfo.extend([
                "",
                "  Note :",
                self.indented_wrap(self.note, 66, "  ")
            ])

        self._nfo.extend([
            "",
            f"──┤    Video    ├─────────────────────────────────────────────[ {len(self.video_tracks):0>2} ]──",
            ""
        ])

        if self.video_tracks:
            for video in self.video_tracks:
                for line in self.get_video_summary(video).splitlines(keepends=False):
                    self._nfo.append(self.indented_wrap(line, 66, "  "))
        else:
            self._nfo.append("  --")

        self._nfo.extend([
            "",
            f"──┤    Audio    ├─────────────────────────────────────────────[ {len(self.audio_tracks):0>2} ]──",
            ""
        ])

        if self.audio_tracks:
            for audio in self.audio_tracks:
                self._nfo.append(self.indented_wrap(self.get_audio_summary(audio), 66, "  "))
        else:
            self._nfo.append("  --")

        self._nfo.extend([
            "",
            f"──┤    Subtitles     ├────────────────────────────────────────[ {len(self.text_tracks):0>2} ]──",
            ""
        ])

        if self.text_tracks:
            for text in self.text_tracks:
                self._nfo.append(self.indented_wrap(self.get_subtitle_summary(text), 66, "  "))
        else:
            self._nfo.append("  --")

        self._nfo.extend([
            "",
            f"──┤    Chapters    ├──────────────────────────────────────────[ {len(self.chapters):0>2} ]──",
            ""
        ])

        for line in self.get_chapter_list(self.chapters) or ["--"]:
            self._nfo.append(self.indented_wrap(line, 66, "  "))

        self._nfo = "\n".join(self._nfo)
        return self._nfo

    @property
    def release_name(self) -> str:
        """The release name used for the output NFO filename."""
        return self.file.stem

    @property
    def file_ext(self) -> str:
        """The file extension to use when saving this template."""
        return ".nfo"
