from abc import abstractmethod

from nfog.templates import Template


class Artwork:
    @staticmethod
    @abstractmethod
    def with_template(template: Template) -> str:
        """Return the Artwork with the Template information."""
