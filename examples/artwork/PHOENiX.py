from nfog.artwork import Artwork
from nfog.templates import Template


class PHOENiX(Artwork):
    @staticmethod
    def with_template(template: Template) -> str:
        return "\n".join([
            "``--.`  :hMMMs`  ..`                            `..  `sMMMh:  `.--``",
            " .-`  :dMMMd-  `.......```                ```.......`  -dMMMd:  `-.",
            "`.  .hMMMMs`          `.---.`         `..---.`          `sMMMMh.  .`",
            "`  /NMMMM+ ./+.   ``...``                  ``...``   .+/. +MMMMN/  `",
            " `sMMMMMdhNMo`  `..`                            `..`  `oMNhmMMMMMs`",
            "`hMMMMMMMMd.  ..`                                  `..  .dMMMMMMMMh`",
            "dMMMMMMMMh` `..                                      ..` `hMMMMMMMMd",
            "MMMMMMMMd` `-`                                        `-` `dMMMMMMMM",
            "MMMMMMMM:  ..                                          ..  :MMMMMMMM",
            "MMMMMMMN  `-                            `               -`  NMMMMMMM",
            "MMMMMMMm  `-                     `......`..`            -`  mMMMMMMM",
            "MMMMMMMN` `-                 `...``    ./-`-`           -` `NMMMMMMM",
            "MMMMMMMM/  ..     `        `..`  ./sooy+.  ..          ..  /MMMMMMMM",
            "MMMMMMMMm` `-`    `--......`  .omMMMMh` `..-.         `-` `mMMMMMMMM",
            "MMMMMMMMMy  `-`    `-.      -smdMMMMm` `-  ``        `-`  yMMMMMMMMM",
            "MMMMMMMMMMy` `..`    ..`    .`.mMMMm-  ..          `..` `yMMMMMMMMMM",
            "MMMMMMMMMMMm:  `.......--.`  /NMMMMN`  ..````.......`  :mMMMMMMMMMMM",
            "NMMMMMMMMMMMMd+.    ``````  .NMMMMMMy` `````````    .+dMMMMMMMMMMMMN",
            "`:ohmMMMMMMMMMMMNhyoo+.    /dMMMMMMMMNy/`    .+ooyhNMMMMMMMMMMMmho:`",
            "ysssyhNMMMMMMMMMMMMMMMMNdyssyhNMMMMMMMdyssydNMMMMMMMMMMMMMMMMmhysssy",
            "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
            "MMMMMMMMmsdMMMMMMMMMNmmMMMM : PHOENiX : MMMMMmmNMMMMMMMMMdsmMMMMMMMM",
            "MMNmhs/..dMMMMMMh+-``oNMMMMMMMMMMMMMMMMMMMMMMNo``-+hMMMMMMd../shmNMM",
            "``    `sMMMMMMy.   /NMMMMmmMMMMMMMMMMMMMMmmMMMMN/   .yMMMMMMs`    ``",
            "    -sNMMMMMN/    oMMMNs--MMMMMMMMMMMMMMMN--sNMMMo    /NMMMMMNs-",
            "`/ymMMMMMMNs`    +MMd/` `dh/MMMMMMMMMMMN/hd` `/dMM+    `sNMMMMMMmy/`",
            "  -/ooso/-  `.  `Nm:    .`  NMMMMMMMMMMN  `.    :mN`  .`  -/osoo/-",
            "..```  ```...-  :m`         hMMMMMMMMMMh         `m:  -...```  ```..",
            "  ``....```  -` `-          -MMMMMMMMMM-          -` `-  ```....``",
            "             ..      ``      +MMMMMMMM+      ``      ..",
            "              ..`  `----.`    :NMMMMN:    `.----   `..",
            "               `..` ------.  ``oMMMMo``  .------ `..`",
            "                 `..-----..  -MmMMMMmM-  ..-----..`",
            "                  `--.`   .+mMMMMMMMMm+.   `.--`",
            "",
            *template.nfo.splitlines(keepends=False)
        ])
