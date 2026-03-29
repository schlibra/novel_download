from ..base_adapter import *

class Xbqg77Adapter(Adapter):
    base_url = 'https://www.xbqg77.com'
    adapter_name = 'xbqg77'

    def parse_book_id(self, url: str) -> str:
        if url.startswith(f'{self.base_url}/'):
            url = url.replace(f'{self.base_url}/', '')
        if url.endswith('/'):
            url = url[:-1]
        return url

    def get_book_data(self) -> BookData:
        res = self.request('get', self.book.url)
        return BookData(
            res.css('div.des>div.text ::text').get(),
            res.css('div.zuthor ::text').get().replace('作者：', ''),
            self.book.url,
            res.css('div.title ::text').get()
        )

    def get_chapter_page(self):
        yield None

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request('get', self.book.url)
        for index, item in enumerate(res.css('div.chapter>ol>li>a').getall()):
            a_ele = self.parse_html(item)
            title = a_ele.css('a ::text').get()
            url = a_ele.css('a').attrib.get('href', '')
            yield ChapterModel(
                title,
                '',
                _book_data.book_name,
                str(index+1),
                url
            )

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        res = self.request('get', chapter.url)
        chapter.content = "\n".join(res.css('#article ::text').getall())
        return chapter

    def search_book(self, keyword: str):
        pass