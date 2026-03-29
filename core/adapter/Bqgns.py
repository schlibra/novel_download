import math

from ..base_adapter import *

class BqgnsAdapter(Adapter):
    base_url = 'https://www.bqgns.com'
    adapter_name = 'Bqgns'

    def parse_book_id(self, url: str) -> str:
        if url.startswith(f'{self.base_url}/book/'):
            url = url.replace(f'{self.base_url}/book/', '')
        if url.endswith('/'):
            url = url[:-1]
        return url

    def get_book_data(self) -> BookData:
        res = self.request(get, '/api/query/get_book_list', params={'bookId': self.book.book_id, 'sort': '0', 'page': '1'}).json()
        data = res.get('data', {})
        return BookData(
            data.get('des', ''),
            data.get('author', ''),
            self.book.url,
            data.get('title', '')
        )


    def get_chapter_page(self):
        res = self.request(get, '/api/query/get_book_list', params={'bookId': self.book.book_id, 'sort': '0', 'page': '1'}).json()
        total = res.get('data', {}).get('update_id', 0)
        return range(math.ceil(total / 100))

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request(get, '/api/query/get_book_list', params={'bookId': self.book.book_id, 'sort': '0', 'page': '1'}).json()
        for item in res.get('data', {}).get('list', []):
            yield ChapterModel(
                item.get('tit', ''),
                '',
                _book_data.book_name,
                item.get('chapter_id', ''),
                f'{self.base_url}/{self.book.book_id}/{item.get("chapter_id", "")}'
            )

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        res = self.request(get, '/api/query/get_book_text', params={'bookId': self.book.book_id, 'id': chapter.order}).json()
        for text in res.get('data', {}).get('text', []):
            chapter.content += self.markdown(text.get('text', ''))
        return chapter

    def search_book(self, keyword: str):
        pass