from ..base_adapter import *

class QiShuXiaAdapter(Adapter):
    base_url = "https://www.qishuxia.com"
    adapter_name = "QiShuXia"

    def parse_book_id(self, url: str) -> str:
        self.request(get, url, skip_error=True)
        if url.startswith(f"{self.base_url}/book/"):
            url = url.replace(f"{self.base_url}/book/", "")
        if url.endswith("/"):
            url = url[:-1]
        return url

    def get_book_data(self) -> BookData:
        res = self.request(get, f"/book/{self.book.book_id}/")
        return BookData(
            res.metadata("og:description"),
            res.metadata("og:novel:author"),
            res.metadata("og:novel:read_url"),
            res.metadata("og:novel:book_name")
        )

    def get_chapter_page(self):
        yield None

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request(get, f"/book/{self.book.book_id}/")
        for index, _li in enumerate(res.css("#section-list li a").getall()):
            _li_ele = self.parse_html(_li)
            _title = _li_ele.css("::text").get()
            _href = _li_ele.css("a").attrib.get("href", "")
            yield ChapterModel(
                _title,
                "",
                _book_data.book_name,
                str(index+1),
                f"{self.book.url}{_href}"
            )

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        res = self.request(get, chapter.url)
        chapter.content = "".join(res.css("#content ::text").getall())
        return chapter

    def search_book(self, keyword: str):
        pass
