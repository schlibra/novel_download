class ChapterModel:
    __title: str
    __content: str
    __book_name: str
    __order: str
    __url: str
    def __init__(self, _title: str, _content: str, _book_name: str, _order: str, _url: str):
        self.__title = _title
        self.__content = _content
        self.__book_name = _book_name
        self.__order = _order
        self.__url = _url

    @staticmethod
    def from_dict(_dict: dict):
        return ChapterModel(
            _dict.get('chaptername', ''),
            '',
            _dict.get('articlename', ''),
            _dict.get('chapterorder', ''),
            _dict.get('chapterurl', '')
        )

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, _title: str):
        self.__title = _title

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, _content: str):
        self.__content = _content

    @property
    def book_name(self) -> str:
        return self.__book_name

    @book_name.setter
    def book_name(self, _book_name: str):
        self.__book_name = _book_name

    @property
    def order(self) -> str:
        return self.__order

    @order.setter
    def order(self, _order: str):
        self.__order = _order

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, _url: str):
        self.__url = _url

    def __str__(self):
        return f"ChapterModel(title='{self.title}', content='{self.content}', book_name='{self.book_name}', order='{self.order}', url='{self.url}')"