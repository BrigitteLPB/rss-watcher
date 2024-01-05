from feedparser import parse, FeedParserDict
from time import mktime
from datetime import datetime, timedelta, timezone
import socket
from socks import set_default_proxy, SOCKS5, socksocket


class RSSWatcher:
    @classmethod
    def setup_tor_proxy(cls, tor_proxy_address: str, tor_proxy_port: int):
        """
        Create a tor proxy
        """
        set_default_proxy(SOCKS5, tor_proxy_address, tor_proxy_port)
        socket.socket = socksocket

    def __init__(
        self, feed_url: str, update_timeout: int = 500, ignore_first: bool = False
    ) -> None:
        """
        update_timeout : time in ms before feed update
        ignore_first : ignore the first news on setup
        """
        self.feed_url = feed_url
        self.last_link = ""
        self.update_timeout = timedelta(milliseconds=update_timeout)
        self._feed_updated_at = datetime.min.replace(tzinfo=timezone.utc)
        self.ignore_first = ignore_first

    @property
    def data(self):
        # update the feed if the timeout is set
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        if now > self._feed_updated_at + self.update_timeout:
            self._feed: FeedParserDict = parse(self.feed_url)
            if not self._feed.feed:
                raise ValueError(
                    f"Cannot initialising feed {self.feed_url}. Check the connection."
                )

            if not self._feed.feed.updated_parsed:
                raise ValueError(f"Can not get update timepstamp for {self.feed_url}")

            self._feed_updated_at = datetime.fromtimestamp(
                mktime(self._feed.feed.updated_parsed)
            ).replace(tzinfo=timezone.utc)

        return self._feed

    def get_news(self) -> list:
        """
        Return all the new entries from the RSS feed
        """
        if not self.ignore_first or self._feed_updated_at != datetime.min.replace(
            tzinfo=timezone.utc
        ):
            for entry in self.data.entries:
                if self.last_link == entry.link:
                    break

                yield entry

        # update the timestamp
        self.last_link = self.data.entries[0].link
        return
