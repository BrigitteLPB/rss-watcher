from os import environ
from rss_watcher import RSSWatcher
from set_interval import SetInterval
import logging
import keyboard
from proxy import Proxy, TorProxy

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("starting ! ~UzU~")

    # load env vars
    feedlist = environ.get("FEEDLIST", "")
    if not feedlist:
        raise ValueError("No feed found ! Check env var FEEDLIST")

    # settings up tor proxy
    if tor_proxy_address := environ.get("TOR_PROXY_ADDRESS", ""):
        proxy = TorProxy()
        proxy.setup_proxy(proxy_address=tor_proxy_address)
    # using default proxy here
    else:
        proxy = Proxy()

    # init all feeds
    feeds = [
        RSSWatcher(feed_url=feed_url, update_timeout=10000, proxy=proxy)
        for feed_url in feedlist.split(",")
    ]

    def parse_feeds():
        """
        Parsing all the feeds
        """
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

    # setup the infinite loop
    interval = SetInterval(interval=10, action=parse_feeds, start_immediatly=True)

    # escape the program with escape key
    print("[Press ECHAP key for finishing the program]")
    keyboard.on_press_key("esc", lambda _: interval.cancel())
    keyboard.wait("esc")
