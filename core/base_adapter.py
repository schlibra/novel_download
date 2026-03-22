from abc import ABC, abstractmethod
from typing import Union

import requests.exceptions
from parsel import Selector
from requests_toolbelt.sessions import BaseUrlSession
from fake_useragent import UserAgent
from .model import *


class Adapter(ABC):
    base_url: str
    book: BookInfo
    session: BaseUrlSession
    adapter_name: str

    def __init__(self, book: BookInfo):
        self.book = book
        if not book.book_id:
            book.book_id = self.parse_book_id(book.url)
        ua = UserAgent().random
        self.session = BaseUrlSession(base_url=self.base_url)
        self.session.headers.update({"User-Agent": ua})

    def request(self, method, url, data=None, json=None, parse=True) -> Response:
        try:
            res = self.session.request(method, url, data=data, json=json)
        except requests.exceptions.RequestException as _e:
            print('Request error, retrying...')
            return self.request(method, url, data=data, json=json, parse=parse)
        if res.ok:
            return Response(res, parse=parse)
        else:
            raise Exception(f"Failed to request {url}, status code: {res.status_code}")

    @staticmethod
    def parse_html(html: str) -> Selector:
        return Selector(text=html)

    @staticmethod
    def markdown(text: Union[str, list]) -> str:
        if isinstance(text, list):
            text = "".join(text)
        if text is None:
            return ""
        import html2text
        return html2text.html2text(text)


    @abstractmethod
    def parse_book_id(self, url: str) -> str:
        pass

    @abstractmethod
    def get_book_data(self) -> BookData:
        pass

    @abstractmethod
    def get_chapter_page(self):
        pass

    @abstractmethod
    def get_chapter_list(self, page_index, _book_data: BookData):
        pass

    @abstractmethod
    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        pass
