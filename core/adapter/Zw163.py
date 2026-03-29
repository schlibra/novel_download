from ..base_adapter import *

class Zw163Adapter(Adapter):
    base_url = 'https://www.163zw.com'
    adapter_name = 'Zw163'

    def parse_book_id(self, url: str) -> str:
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
        if page_text := res.css('div.pages>ul>li:nth-of-type(1)>a ::text').get():
            if '/' in page_text:
                page_num = int(page_text.split('/')[1])
            else:
                page_num = 1
        else:
            page_num = 1
        return range(1, page_num+1)

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request('get', f'{self.book.url}index_{page_index}.html')
        for index, item in enumerate(res.css('section:nth-of-type(3) div.book_list>ul>li>a').getall()):
            a_ele = self.parse_html(item)
            title = a_ele.css('a ::text').get()
            url = a_ele.css('a').attrib.get('href', '')
            yield ChapterModel(
                title,
                '',
                _book_data.book_name,
                str((int(page_index)-1)*100+index+1),
                url
            )

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        res = self.request('get', chapter.url)
        for line in res.css('article ::text').getall():
            if _line := self.markdown(line).strip():
                chapter.content += _line + '\n'
        return chapter

    def search_book(self, keyword: str):
        pass