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
        ua = UserAgent().random
        self.session = BaseUrlSession(base_url=self.base_url)
        self.session.headers.update({"User-Agent": ua})
        if not book.book_id:
            book.book_id = self.parse_book_id(book.url)

    def request(self, method, url, data=None, json=None, headers=None, parse=True, skip_error=False) -> Response:
        if not headers:
            headers = {}
        try:
            res = self.session.request(method, url, data=data, json=json, headers=headers)
        except requests.exceptions.RequestException as _e:
            print('Request error, retrying...')
            return self.request(method, url, data=data, json=json, parse=parse)
        if res.ok:
            return Response(res, parse=parse)
        else:
            if not skip_error:
                raise Exception(f"Failed to request {url}, status code: {res.status_code}")
            else:
                return Response(res, parse=parse)

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

    @abstractmethod
    def search_book(self, keyword: str):
        pass
