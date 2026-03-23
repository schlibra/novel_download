class BookInfo:
    __site: str
    __url: str
    __book_id: str
    __skip: bool
    __book_name: str
    __author: str
    def __init__(self, _site="", _url="", _book_id="", _skip=False, _book_name="", _author=""):
        self.__site = _site
        self.__url = _url
        self.__book_id = _book_id
        self.__skip = _skip
        self.__book_name = _book_name
        self.__author = _author

    @property
    def site(self):
        return self.__site

    @site.setter
    def site(self, _site):
        self.__site = _site

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, _url):
        self.__url = _url

    @property
    def book_id(self):
        return self.__book_id

    @book_id.setter
    def book_id(self, _book_id):
        self.__book_id = _book_id

    @property
    def skip(self):
        return self.__skip

    @skip.setter
    def skip(self, _skip):
        self.__skip = _skip

    @property
    def book_name(self):
        return self.__book_name

    @book_name.setter
    def book_name(self, _book_name):
        self.__book_name = _book_name

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, _author):
        self.__author = _author

    @staticmethod
    def from_dict(_data):
        return BookInfo(
            _data.get('site', ''),
            _data.get('url', ''),
            _data.get('book_id', ''),
            _data.get('skip', False)
        )

    def __str__(self):
        site = self.site
        url = self.url
        book_id = self.book_id
        skip = self.skip
        book_name = self.book_name
        author = self.author
        return f"BookInfo({site=}, {url=}, {book_id=}, {skip=}, {book_name=}, {author=})"