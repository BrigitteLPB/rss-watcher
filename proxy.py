import requests
from datetime import datetime, timedelta
from stem import Signal
from stem.control import Controller


class Proxy:
    def setup_proxy(self, proxy_address: str):
        self.proxy = {
            "http": proxy_address,
            "https": proxy_address,
        }

    def get(self, url: str) -> str:
        if self.proxy:
            return requests.get(url=url, proxies=self.proxy).text
        return requests.get(url=url).text


class TorProxy(Proxy):
    def get(self, url: str) -> str:
        if not self.proxy:
            raise ValueError("Can not run Tor without setuped proxies")
        return requests.get(url=url, proxies=self.proxy).text
