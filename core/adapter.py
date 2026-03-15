from abc import abstractmethod, ABC
from parsel import Selector
import re
import html2text
from fake_useragent import UserAgent

from requests_toolbelt.sessions import BaseUrlSession

class Adapter(ABC):
    BASE_URL: str
    __BOOK_ID: str
    __SESSION: BaseUrlSession
    def __init__(self, book_url: str):
        self.parse_book_id(book_url)
        _ua = UserAgent().random
        self.session = BaseUrlSession(base_url=self.base_url)
        self.session.headers.update({
            "User-Agent": _ua,
        })
    @abstractmethod
    def parse_book_id(self, book_url: str):
        pass
    @abstractmethod
    def get_book_info(self):
        pass
    @abstractmethod
    def get_chapter_content(self, page_num: int):
        pass
    @property
    def base_url(self) -> str:
        return self.BASE_URL
    @property
    def book_id(self):
        return self.__BOOK_ID
    @book_id.setter
    def book_id(self, _book_id):
        self.__BOOK_ID = _book_id
    @property
    def session(self) -> BaseUrlSession:
        return self.__SESSION
    @session.setter
    def session(self, _session):
        self.__SESSION = _session
    @staticmethod
    def get_meta(_res_text: str, meta_name: str):
        _html = Selector(_res_text)
        if _ele := _html.xpath(f"//meta[@property='{meta_name}']"):
            return _ele.attrib.get('content')
        else:
            return None
    @staticmethod
    def parse_book_info(_res_text: str, attr_list: list[dict[str, str]]):
        _info = {}
        for item in attr_list:
            key = list(item.keys())[0]
            value = item[key]
            _info[key] = Adapter.get_meta(_res_text, value)
        return _info
