class BookData:
    __description = ""
    __author = ""
    __book_url = ""
    __book_name = ""
    def __init__(self, _description, _author, _book_url, _book_name):
        self.__description = _description
        self.__author = _author
        self.__book_url = _book_url
        self.__book_name = _book_name

    @property
    def description(self):
        return self.__description

    @property
    def author(self):
        return self.__author

    @property
    def book_url(self):
        return self.__book_url

    @property
    def book_name(self):
        return self.__book_name

    @description.setter
    def description(self, _description):
        self.__description = _description

    @author.setter
    def author(self, _author):
        self.__author = _author

    @book_url.setter
    def book_url(self, _book_url):
        self.__book_url = _book_url

    @book_name.setter
    def book_name(self, _book_name):
        self.__book_name = _book_name

    def __str__(self):
        return f"BookData(description={self.__description}, author={self.__author}, book_url={self.__book_url}, book_name={self.__book_name})"
