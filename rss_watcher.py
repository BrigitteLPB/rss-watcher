from feedparser import parse, FeedParserDict
from time import mktime
from datetime import datetime, timedelta, timezone
from requests import session, Session, RequestException, get
import logging
from proxy import Proxy

logger = logging.getLogger(__name__)


class RSSWatcher:
    def __init__(
        self,
        feed_url: str,
        update_timeout: int = 500,
        ignore_first: bool = False,
        proxy: Proxy = None,
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
        self.proxy = proxy or Proxy()

    @property
    def data(self):
        # update the feed if the timeout is set
        now = datetime.utcnow().replace(tzinfo=timezone.utc)

        if now > self._feed_updated_at + self.update_timeout:
            try:
                self._feed: FeedParserDict = parse(self.proxy.get(self.feed_url))
            except RequestException as e:
                logger.error(f"Connection error for the RSS feed {self.feed_url}")
                logger.exception(e)
                raise e

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
