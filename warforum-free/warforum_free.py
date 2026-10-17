"""FatRat download plugin for webshare.cz links (free tier).

Handles links like https://webshare.cz/#/file/5ShDjqTwK2/ddo02-7z
"""

import re

import fatrat

URL_PATTERN = r"https?://(?:www\.)?webshare\.cz/#/file/[^/]+/[^/\s]+"


@fatrat.download_plugin(
    name="Warforum free",
    url_pattern=URL_PATTERN,
    single_transfer=True,
    truncate_incomplete=False,
)
class WarforumFree(fatrat.DownloadPlugin):

    async def process_link(self, url: str) -> None:
        match = re.search(r"/#/file/([^/]+)/([^/\s]+)", url)
        if not match:
            raise fatrat.PluginError("unrecognised webshare.cz link")

        self.vars["ident"] = match.group(1)
        self.vars["slug"] = match.group(2)

        # TODO: resolve the download link (to be specified).
        raise fatrat.PluginError("not implemented yet")
