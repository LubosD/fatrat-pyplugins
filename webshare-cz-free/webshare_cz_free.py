"""FatRat download plugin for webshare.cz links (free tier).

Handles links like https://webshare.cz/#/file/5ShDjqTwK2/ddo02-7z
"""

import re
import urllib.parse
import uuid
import xml.etree.ElementTree as ET

import fatrat

URL_PATTERN = r"https?://(?:www\.)?webshare\.cz/#/file/[^/]+/[^/\s]+"
API_URL = "https://webshare.cz/api/file_link/"


@fatrat.download_plugin(
    name="Webshare.cz free",
    url_pattern=URL_PATTERN,
    single_transfer=True,
    truncate_incomplete=False,
)
class WebshareCzFree(fatrat.DownloadPlugin):

    async def process_link(self, url: str) -> None:
        match = re.search(r"/#/file/([^/]+)/([^/\s]+)", url)
        if not match:
            raise fatrat.PluginError("unrecognised webshare.cz link")

        ident = match.group(1)
        self.vars["ident"] = ident

        response = await self.fetch(API_URL, data={
            "ident": ident,
            "password": "",
            "download_type": "file_download",
            "force_https": "1",
            "device_uuid": str(uuid.uuid4()),
            "device_res_x": "1920",
            "device_res_y": "1080",
            "wst": "",
        })

        try:
            root = ET.fromstring(response.text)
        except ET.ParseError:
            raise fatrat.PluginError("webshare.cz returned an unreadable response")

        status = (root.findtext("status") or "").strip()
        link = (root.findtext("link") or "").strip()
        if status != "OK" or not link:
            reason = (root.findtext("message") or status or "no link in the response").strip()
            raise fatrat.PluginError(f"webshare.cz refused the download: {reason}")

        name = urllib.parse.unquote(urllib.parse.urlparse(link).path.rsplit("/", 1)[-1])
        if name:
            self.report_file_name(name)

        self.start_download(fatrat.DownloadUrl(url=link, referrer="https://webshare.cz/"))
