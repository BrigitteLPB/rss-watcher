from os import environ
from rss_watcher import RSSWatcher
from set_interval import SetInterval
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("starting ! ~UzU~")

    # load env vars
    feedlist = environ.get("FEEDLIST", "")
    if not feedlist:
        raise ValueError("No feed found ! Check env var FEEDLIST")

    # settings up tor proxy
    if tor_proxy_address := environ.get("TOR_PROXY_ADDRESS", ""):
        RSSWatcher.setup_tor_proxy(tor_proxy_address=tor_proxy_address)

    feeds = [
        RSSWatcher(feed_url=feed_url, update_timeout=10000)
        for feed_url in feedlist.split(",")
    ]

    def parse_feeds():
        for feed in feeds:
            try:
                for entry in feed.get_news():
                    print("-----------------------------------------------")
                    print(f">>> <{feed.feed_url}>'s news")
                    print(f"Titre: {entry.get('title', '')}")
                    print(f"Description: {entry.get('summary', '')}")
                    print(f"Lien: {entry.get('link', '')}")
                    print(f"Date: {entry.get('updated', '')}")
                    print()

            except Exception as e:
                logger.error(f"Error while fetchning news on {feed.feed_url}")
                logger.exception(e)

    SetInterval(interval=10, action=parse_feeds, start_immediatly=False)
