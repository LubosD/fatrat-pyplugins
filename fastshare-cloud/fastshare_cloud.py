"""FatRat download plugin for fastshare.cloud links (free tier).
"""

import html
import re

import fatrat

URL_PATTERN = r"https?://(?:www\.)?fastshare\.cloud/\d+/[^/\s]+"


@fatrat.download_plugin(
    name="FastShare.cloud free",
    url_pattern=URL_PATTERN,
    single_transfer=True,
    truncate_incomplete=True,
)
class FastshareCloud(fatrat.DownloadPlugin):

    async def process_link(self, url: str) -> None:
        match = re.search(r"fastshare\.cloud/(\d+)/([^/\s?#]+)", url)
        if not match:
            raise fatrat.PluginError("unrecognised fastshare.cloud link")

        self.vars["id"] = match.group(1)

        # The file page sets the session cookies the free link needs.
        page = await self.fetch(url)
        free = page.search(r'href="(/free/\?[^"]+)"[^>]*id="?free-trigger')
        if not free:
            raise fatrat.PluginError("fastshare.cloud offers no free download for this file")

        name = page.search(r'<h1 title="([^"]+)"')
        name = html.unescape(name).strip() if name else match.group(2)
        self.report_file_name(name)

        # The free link redirects to a one-off URL on a data server; FatRat
        # follows that redirect itself, so the file isn't fetched twice.
        self.start_download(fatrat.DownloadUrl(url=page.urljoin(html.unescape(free)),
                                               referrer=url, file_name=name))
