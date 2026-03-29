from ..base_adapter import *

class SuDuGuAdapter(Adapter):
    base_url = 'https://www.sudugu.org'
    adapter_name = 'SuDuGu'

    def parse_book_id(self, url: str) -> str:
        if url.startswith(f'{self.base_url}/'):
            url = url.replace(f'{self.base_url}/', '')
        if url.endswith('/'):
            url = url[:-1]
        return url

    def get_book_data(self) -> BookData:
        res = self.request(get, self.book.url)
        description = '\n'.join(res.css('div.des.bb ::text').getall())
        author = res.css('div.container>div.item>div.itemtxt>p:nth-of-type(2) ::text').get().replace('作者：', '')
        title = res.css('div.container>div.item>div.itemtxt>h1>a ::text').get()
        return BookData(
            description,
            author,
            self.book.url,
            title
        )

    def get_chapter_page(self):
        res = self.request(get, self.book.url)
        for index, _ in enumerate(res.css('#pageSelect>option').getall()):
            yield str(index + 1)

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request(get, f'{self.book.url}p-{page_index}.html')
        for index, item in enumerate(res.css('#list li').getall()):
            title = self.parse_html(item).css('a ::text').get()
            link = self.parse_html(item).css('a').attrib.get('href', '')
            yield ChapterModel(
                title,
                '',
                _book_data.book_name,
                str((int(page_index) - 1) * 1000 + index + 1),
                link
            )

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        print(chapter)
        res = self.request(get, chapter.url)
        chapter.content = '\n'.join(res.css('div.container>div.con ::text').getall())
        return chapter

    def search_book(self, keyword: str):
        pass