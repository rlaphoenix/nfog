import textwrap
from datetime import datetime

from nfog.artwork import Artwork
from nfog.templates import Template


class MiU(Artwork):
    @staticmethod
    def with_template(template: Template) -> str:
        rls_name = textwrap.wrap(template.release_name, 50)
        rls_name = [
            rls_name[0] if len(rls_name) > 1 else '    °。  .                  .+',
            rls_name[len(rls_name) - 1]
        ]
        now = datetime.now().strftime("%Y.%m.%d %H:%M")
        nfo = template.nfo.splitlines(keepends=False)
        is_nfo = template.file_ext == ".nfo"

        art = [
            "。                  *              °               °。               +  ",
            "   *     °。       ⢀⡴⠞⢳                                                ",
            "      .          ⡔⠋ ⢰⠎    ..     MiU PROUDLY PRESENTS      °。         ",
            "   °。    .。    ⣼⢆⣤⡞⠃                                  。               ",
           f"        *       ⣼⢠⠋⠁ {rls_name[0]}",  # noqa: E131
           f"   。  ⢀⣀⣾⢳    ⢸⢠⠃  {rls_name[1]}",
            "  ⣀⡤⠴⠊⠉  ⠈⠳⡀  ⠘⢎⠢⣀⣀⣀       .                                          ",
            "  ⠳⣄  ⡠⡤⡀ ⠘⣇⡀   ⠉⠓⠒⠺⠭⢵⣦⡀     *      °。                    °           ",
            "   ⢹⡆ ⢷⡇⠁  ⣸⠇  。  ⢠⢤  ⠘⢷⣆⡀                    *    .           *      ",
            "    ⠘⠒⢤⡄⠖⢾⣭⣤⣄ ⡔⢢ ⡀⠎⣸    ⠹⣿⡀  GREETS:                    *             ",
            "  . ⢀⡤⠜⠃  ⠘⠛⣿⢸ ⡼⢠⠃⣤⡟     ⣿⡇   -RPG, -playWEB                          ",
            "    ⠸⠶⠖⢏  ⢀⡤⠤⠇⣴⠏⡾⢱⡏⠁    ⢠⣿⠃                       *       +           ",
            "       ⠈⣇⡀⠿    ⡽⣰⢶⡼⠇    ⣠⣿⠟    °。    *                                ",
            "  +.    ⠈⠳⢤⣀⡶⠤⣷⣅⡀   ⣀⡠⢔⠕⠁                     °。     *      。         ",
            "     。    °。  ⠈⠙⠫⠿⠿⠿⠛⠋⠁   .+     °               .                    "
        ]

        footer = [
            "{ MiU x nfog }".center(70),
            now.center(70)
        ]

        if not is_nfo:
            nfo = [
                "[align=center]",
                *[
                    x.ljust(70, " ")
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