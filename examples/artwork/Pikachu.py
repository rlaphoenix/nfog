from nfog.artwork import Artwork
from nfog.templates import Template


class Pikachu(Artwork):
    @staticmethod
    def with_template(template: Template) -> str:
        return "\n".join([
            "                                  :++++++++++++.",
            "                            .ooooohmmmmmmmmmmmmyooooo",
            "                     +ooooooymmmmmmmmmmmmmmmmmmmmmmmmooooooo:",
            "                 /sssdmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmhsss.",
            "             -yyydmmmmm-:mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmy-+mmmmmhyyy",
            "          ```:mmmmmmmmm `mmmmmo   ymmmmmmmmmmmmm   dmmmmy :mmmmmmmmm``",
            "       ```` ``ommm:```hhmy   nhhhdmmmmh` mmmmmdhhhn   mdho```smmm-` ``",
            "    ` `````` ` ```    mmmmddddmmmmmmmmmddmmmmmmmmmddddmmmo    ``` `` `",
            "                     ``mmddddmmmmmmmdd     :ddmmmmmmmddddms`",
            "                     hmdh   oddmmmmm`        +mmmmmdd   +ddm+",
            "  `.........         hm       smmmmm`        +mmmmm+      om+",
            "  .mmmmmmmmh-----`   hmo+    oymmmmm`        :yyydmoo    oym+",
            "  .mmmmmmmmmmmmmmo:` hmmdoooymmmmmmm/:     . .   osdmooosmmm+",
            "  .mmmmmmmmmmmmmmmm+:oommmmmmmmmmmmmmm:::::- +mmm+ oommmmmho:",
            "  .mmmmmmmmmmmmmmmmmm` mmmmmmmmmmmmmmmmmmmmy +ohmmm+  ommmo",
            "  :++++++++mmmmmmmmmm` +ommmmmmmmmmmmmmmmmmmmy ++hmmm++ ++:",
            "           //smmmmmmm` oommmmmmmmmmmhh::::::hdm: ymmmmh  o:",
            "                :ymmm` mmmmmmms:ymmmddyymmyhddmyo :dmmdos o",
            "             -ssshm+:  mmmmmmm+ ommmmmddddddmmmmm- hmmmmmmo",
            "          yyyhmo---` symmmmmmm+ ommmmmmmmmmmmmmmmhydmmmmmmdy:",
            "      shhhmy...`     hmmd /mmmdh .ymmmmmmmmmmmmmmmmmmmmmmmmm+",
            "      ```-mdhhh/     hmmh -mmmmm: ymmmmmmmmmmmmmmmmmmmmmmmmm+",
            "          ```/mdddd- hmmmds /mmm: ymmmmmmmmmmmmmmmmmmmmmmmmm+",
            "",
            *template.nfo.splitlines(keepends=False)
        ])
