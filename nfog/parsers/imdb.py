import json
import re
from typing import Any

from requests import Session


class IMDb:
    def __init__(self, title_id: str):
        """
        Parameters:
            title_id: The IMDb Title ID excluding the `tt`.
        """
        super().__init__()

        self.id = title_id
        self.session = self._get_session()

    def get_title_data(self) -> dict[str, Any]:
        payload = self._get_payload(f"https://www.imdb.com/title/tt{self.id}")

        data = payload["props"]["pageProps"]

        return {
            "aboveTheFoldData": data["aboveTheFoldData"],
            "mainColumnData": data["mainColumnData"]
        }

    def get_episodes(self, season: int) -> list[dict[str, Any]]:
        payload = self._get_payload(f"https://www.imdb.com/title/tt{self.id}/episodes/?season={season}")

        content_data = payload["props"]["pageProps"]["contentData"]
        if not content_data["entityMetadata"]["titleType"]["canHaveEpisodes"]:
            return []

        section_data = content_data["section"]
        if not any(x["value"] == str(season) for x in section_data["seasons"]):
            raise ValueError(f"Title does not have a Season {season}")

        episode_data = section_data["episodes"]
        if episode_data["hasNextPage"]:
            pass#raise NotImplementedError("This Season has multiple pages of Episodes, cannot continue")

        episode_items = episode_data["items"]

        return episode_items

    def _get_payload(self, url: str) -> dict[str, Any]:
        res = self.session.get(url)
        res.raise_for_status()

        source = res.text
        match = re.search(
            r"<script id=\"__NEXT_DATA__\" type=\"application/json\">(.+)</script>",
            source,
            re.MULTILINE
        )
        if not match:
            raise ValueError(f"Couldn't find the Payload on {url}, did IMDb change something?")

        captured_script = match.group(1).split("</script>")[0]

        payload = json.loads(captured_script)

        return payload

    @staticmethod
    def _get_session() -> Session:
        session = Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
        })
        return session
