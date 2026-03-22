from ..base_adapter import *
from ..model import *


class Bqg475Adapter(Adapter):
    base_url = 'https://www.bqg475.cc'
    adapter_name = 'bqg475'

    def parse_book_id(self, url: str) -> str:
        if url.startswith(f"{self.base_url}/#/book/"):
            url = url.replace(f"{self.base_url}/#/book/", "").replace("/", "")
            if url.endswith("/"):
                url = url[:-1]
        return url

    def get_book_data(self):
        res = self.request('get', f"https://apibi.cc/api/book?id={self.book.book_id}").json()
        return BookData(
            res.get('intro', ''),
            res.get('author', ''),
            f"{self.base_url}/#/book/{self.book.book_id}/",
            res.get('title', '')
        )

    def get_chapter_page(self):
        yield None

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request('get', f'https://apibi.cc/api/booklist?id={self.book.book_id}').json()
        for index, chapter in enumerate(res.get('list', [])):
            i = str(index + 1)
            yield ChapterModel(
                chapter,
                '',
                _book_data.book_name,
                i,
                f"/#/book/{self.book.book_id}/{i}.html"
            )

    def get_chapter_content(self, chapter: ChapterModel):
        res = self.request('get', f'https://apibi.cc/api/chapter?id={self.book.book_id}&chapterid={chapter.order}').json()
        chapter.content = res.get('txt', '')
        return chapter

