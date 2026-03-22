class BookInfo:
    __site: str
    __url: str
    __book_id: str
    __skip: bool
    def __init__(self, _site, _url, _book_id, _skip=False):
        self.__site = _site
        self.__url = _url
        self.__book_id = _book_id
        self.__skip = _skip

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

    @staticmethod
    def from_dict(_data):
        return BookInfo(
            _data.get('site', ''),
            _data.get('url', ''),
            _data.get('book_id', ''),
            _data.get('skip', False)
        )

    def __str__(self):
        return f"BookInfo(site={self.__site}, url={self.__url}, book_id={self.__book_id}, skip={self.__skip})"