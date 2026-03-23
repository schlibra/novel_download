from typing import Any

from parsel import Selector
from requests import Response as _Response


class Response:
    res: _Response
    selector: Selector
    def __init__(self, res: _Response, parse: bool = True):
        self.res = res
        if parse:
            self.selector = Selector(res.text)
    def json(self) -> dict[str, Any]:
        return self.res.json()
    def xpath(self, query: str):
        return self.selector.xpath(query)
    def css(self, query: str):
        return self.selector.css(query)
    def metadata(self, key: str):
        if data := self.selector.xpath(f"//meta[@name='{key}']/@content").get():
            return data
        if data := self.selector.xpath(f"//meta[@property='{key}']/@content").get():
            return data
        return key
    @property
    def cookies(self):
        return self.res.cookies
    def __str__(self):
        return self.res.text