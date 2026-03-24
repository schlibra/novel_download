from ..base_adapter import *

class XslcaAdapter(Adapter):
    base_url = 'https://www.xslca.cc'
    adapter_name = 'Xslca'

    def parse_book_id(self, url: str) -> str:
        if url.startswith(f'{self.base_url}/'):
            url = url.replace(f'{self.base_url}/', '')
        if url.endswith('.html'):
            url = url.replace('.html', '')
        if '/' in url:
            url = url.split('/')[-1]
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
        yield None
    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request('get', _book_data.book_url)
        main_index = 0
        chapter_list = res.css('#list dl').get().split('\n')
        for index, item in enumerate(chapter_list):
            if '正文' in item:
                main_index = index
        chapter_list = chapter_list[main_index+1:]
        for index, chapter in enumerate(chapter_list):
            html = self.parse_html(chapter)
            link = html.css('a').attrib.get('href')
            title = html.css('a::text').get()
            if link and title:
                yield ChapterModel(
                    title,
                    '',
                    _book_data.book_name,
                    str(index+1),
                    link
                )

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        res = self.request('get', chapter.url)
        chapter.content = "".join(res.css('#content::text').getall())
        return chapter

    def search_book(self, keyword: str):
        pass