from os import environ
from rss_watcher import RSSWatcher
from set_interval import SetInterval


if __name__ == "__main__":
    print("starting ! ~UzU~")

    # load env vars
    feedlist = environ.get("FEEDLIST", "")
    if not feedlist:
        raise ValueError("No feed found ! Check env var FEEDLIST")

    feeds = [RSSWatcher(feed_url=feed_url, update_timeout=10000) for feed_url in feedlist.split(',')]

    def parse_feeds():
        for feed in feeds:
            for entry in feed.get_news():
                print('-----------------------------------------------')
                print(f">>> {feed.data.feed.get('title', '')}'s news")
                print(f"Titre: {entry.get('title', '')}")
                print(f"Description: {entry.get('summary', '')}")
                print(f"Lien: {entry.get('link', '')}")
                print(f"Date: {entry.get('updated', '')}")
                print()

    SetInterval(interval=20, action=parse_feeds)
