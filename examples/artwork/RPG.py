from nfog.artwork import Artwork
from nfog.templates import Template


class RPG(Artwork):
    @staticmethod
    def with_template(template: Template) -> str:
        return "\n".join([
            "``````````````````````````````````````````````````````````````````````",
            "``````````````````````````````````````````````````````````````````````",
            "````````````-ddddddddddddd/`ddddddddddddds````:dddddddddd`````````````",
            "````````````:MMMNNNNNNNMMM+`NMMNNNNNNNMMMh`.--/NNNNNNNNNm`````````````",
            "````````````:MMM:``````MMM+`NMMo``````hMMh`yMMd```````````````````````",
            "````````````:MMMs++++++yyy:`NMMh++++++mMMh`yMMd```````````````````````",
            "````````````:MMMMMMMMMM`````NMMMMMMMMMMMMh`yMMd```````````````````````",
            "````````````:MMMMMMh///`````NMMy/////////:`yMMd```yhhhhhh`````````````",
            "````````````:MMMMMMy````````NMMo```````````yMMd```mMMMMMM`````````````",
            "````````````:MMM:``oMMM`````NMMo``-MMM/````yMMd``````oMMM`````````````",
            "````````````:MMM:``/hhh///-`NMMo``.hhh:````ohhy//////ohhh`````````````",
            "````````````:MMM:``````MMM+`NMMo``````````````:MMMMMMs````````````````",
            "````````````.ooo.``````ooo-`+oo:``````````````-ooo+++:````````````````",
            "``````````````````````````````````````````````````````````````````````",
            "``````````````````````` RETRO PRODUCTION GROUP ```````````````````````",
            "`````````````````````````` PROUDLY PRESENTS ``````````````````````````",
            "``````````````````````````````````````````````````````````````````````",
            "``````````````````````````````````````````````````````````````````````",
            "",
            *template.nfo.splitlines(keepends=False),
            "",
            "RPG is currently looking for DVD REMUXers and DVD suppliers.",
            "Get in contact if you feel you have something to offer.",
            "",
            "``````````````````````````````````````````````````````````````````````",
            "``````````````````````````````````````````````````````````````````````"
        ])
