from datetime import datetime

from nfog.artwork import Artwork
from nfog.templates import Template


class MiU(Artwork):
    @staticmethod
    def with_template(template: Template) -> str:
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
            "  . ⢀⡤⠜⠃  ⠘⠛⣿⢸ ⡼⢠⠃⣤⡟     ⣿⡇   -RPG, -playWEB                          ",
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
                    x.ljust(max(70, [70, release_name_width][" : " in x]), " ")
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
