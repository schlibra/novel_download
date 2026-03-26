from ..base_adapter import *

class KanShuLaoAdapter(Adapter):
    base_url = 'https://www.kanshulao.com'
    adapter_name = 'KanShuLao'

    def parse_book_id(self, url: str) -> str:
        if url.startswith(f'{self.base_url}/index/'):
            url = url.replace(f'{self.base_url}/index/', '')
        if url.endswith('/'):
            url = url[:-1]
        return url

    def get_book_data(self) -> BookData:
        res = self.request('get', self.book.url)
        return BookData(
            res.metadata('og:description'),
            res.metadata('og:novel:author'),
            res.metadata('og:novel:read_url'),
            res.metadata('og:novel:book_name')
        )

    def get_chapter_page(self):
        res = self.request('get', self.book.url)
        for index, _ in enumerate(res.css('select#indexselect>option').getall()):
            yield str(index+1)

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request('get', f'{_book_data.book_url}{page_index}')
        for index, item in enumerate(res.css('div.row-section>div.layout>div.section-box:nth-of-type(2)>ul>li').getall()):
            link = self.parse_html(item).css('a').attrib.get('href', '')
            title = self.parse_html(item).css('a::text').get()
            yield ChapterModel(
                title,
                '',
                _book_data.book_name,
                str((int(page_index) - 1) * 50 + index + 1),
                link
            )

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        def remove_ads(_content: str):
            if '搜索本文首发' in _content:
                _content = _content[:_content.index('搜索本文首发')]
            return _content
        res = self.request('get', chapter.url)
        for line in res.css('#content ::text').getall():
            chapter.content += remove_ads(line)
        return chapter

    def search_book(self, keyword: str):
        pass