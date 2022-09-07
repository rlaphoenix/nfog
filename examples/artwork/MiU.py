import re
from datetime import datetime

from nfog.artwork import Artwork
from nfog.templates import Template


class MiU(Artwork):
    @staticmethod
    def with_template(template: Template) -> str:
        """
        The Goal of this Artwork Template is to be a stylish "modern" BBCode NFO.

        It transforms the NFO Template to be a width of 70 characters. It may extend
        the width beyond 70 characters in some sections if the Release name is longer
        than 70 characters.

        Without the padding the text would be aligned centered, which is expected. E.g.:
        |          hey          |
        |      how are you      |

        But I want to center the "block" of content, not the text:
        |      hey........      |
        |      how are you      |
        (notice the `.` represents the padded spaces, padding to 11 characters)
        """
        now = datetime.now().strftime("%Y.%m.%d %H:%M")
        nfo = template.nfo.splitlines(keepends=False)
        is_nfo = template.file_ext == ".nfo"

        art = [
            "。                  *              °               °。               +  ",
            "   *     °。       ⢀⡴⠞⢳                                                ",
            "      .          ⡔⠋ ⢰⠎    ..      °。         +                *       ",
            "   °。    .。    ⣼⢆⣤⡞⠃                                  。               ",
            "        *       ⣼⢠⠋⠁     °。     MiU PROUDLY PRESENTS             °    ",
            "   。  ⢀⣀⣾⢳    ⢸⢠⠃      .                                 +            ",
            "  ⣀⡤⠴⠊⠉  ⠈⠳⡀  ⠘⢎⠢⣀⣀⣀       .                °                         ",
            "  ⠳⣄  ⡠⡤⡀ ⠘⣇⡀   ⠉⠓⠒⠺⠭⢵⣦⡀     *      °。                    °           ",
            "   ⢹⡆ ⢷⡇⠁  ⣸⠇  。  ⢠⢤  ⠘⢷⣆⡀                    *    .           *      ",
            "    ⠘⠒⢤⡄⠖⢾⣭⣤⣄ ⡔⢢ ⡀⠎⣸    ⠹⣿⡀  GREETS:                    *             ",
            "  . ⢀⡤⠜⠃  ⠘⠛⣿⢸ ⡼⢠⠃⣤⡟     ⣿⡇   -RPG, -playWEB, -FLUX             .     ",
            "    ⠸⠶⠖⢏  ⢀⡤⠤⠇⣴⠏⡾⢱⡏⠁    ⢠⣿⠃                       *       +           ",
            "       ⠈⣇⡀⠿    ⡽⣰⢶⡼⠇    ⣠⣿⠟    °。    *                                ",
            "  +.    ⠈⠳⢤⣀⡶⠤⣷⣅⡀   ⣀⡠⢔⠕⠁                     °。     *      。         ",
            "     。    °。  ⠈⠙⠫⠿⠿⠿⠛⠋⠁   .+     °               .                    "
        ]

        footer = (
            # we have to use .center() here, as I actually want it centered
            x.center(70)
            for x in (
                "{ MiU x nfog }",
                now
            )
        )

        release_name_width = len("Release  : ") + len(template.release_name)

        if not is_nfo:
            nfo = [
                "[align=center]",
                *[
                    [
                        x.ljust(max(70, [70, release_name_width][" : " in x]), " "),
                        x  # no need to pad if empty, full of spaces, or ends with a bbcode tag
                    ][not x or x.count(" ") == len(x) or re.search(r"\[/?\w+?(?:=\w+)?]$", x) is not None]
                    for x in (
                        *art,
                        "",
                        *nfo,
                        "\n[hr][/hr]\n",
                        *footer)
                ],
                "[/align]"
            ]
        else:
            nfo = [
                *art,
                "",
                *nfo[2:],  # exclude release name
                "",
                "-- --".center(70),
                *footer
            ]

        nfo = "\n".join(nfo)

        return nfo
