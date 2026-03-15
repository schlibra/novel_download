from core.adapter import *

class ShuYouSheAdapter(Adapter):
    BASE_URL = 'https://www.shuyous.com'

    def parse_book_id(self, book_url: str):
        if book_url.startswith(self.base_url + '/book/') and book_url.endswith('.html'):
            self.book_id = book_url.replace(self.base_url + '/book/', '').replace('.html', '')
        else:
            self.book_id = book_url

    def get_book_info(self):
        _res = self.session.get(f'/book/{self.book_id}.html')
        if _res.ok:
            book_info = self.parse_book_info(_res.text, [
                {'book_name': 'og:novel:book_name'},
                {'book_desc': 'og:description'},
                {'book_author': 'og:novel:author'}
            ])
            total_chapters = self.get_meta(_res.text, 'og:novel:latest_chapter_name')
            _count = re.search(r'(\d+)', total_chapters).group()
            book_info['total_chapters'] = int(_count)
            return book_info
        else:
            raise Exception('Failed to get book info')

    def get_chapter_content(self, page_num: int):
        _res = self.session.get(f'/book/{self.book_id}-{page_num}.html')
        if _res.ok:
            html = Selector(_res.text)
            _title = html.css('.wrap>.con>.readBox>.readCon>.title::text').get()
            _content = html.css('.wrap>.con>.readBox>.readCon>.content').getall()[0]
            _text = html2text.html2text(_content)
            _text = _text[:_text.find(f"({self.base_url}")][:_text.find(f"({self.base_url.replace('https', 'http')}")]
            return {
                'chapter_title': _title,
                'chapter_content': _text
            }
        else:
            raise Exception(f'Failed to get chapter {page_num} content')
