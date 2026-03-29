from ..base_adapter import *

class ShuYouSheAdapter(Adapter):
    base_url = "https://www.shuyous.com"
    adapter_name = "ShuYouShe"

    def parse_book_id(self, url: str) -> str:
        if url.startswith(f"{self.base_url}/book/") and url.endswith(".html"):
            url = url.replace(f"{self.base_url}/book/", "").replace(".html", "")
        return url

    def get_book_data(self) -> BookData:
        res = self.request(get, f"/book/{self.book.book_id}.html")
        return BookData(
            res.metadata("description"),
            res.metadata("og:novel:author"),
            res.metadata("og:novel:read_url"),
            res.metadata("og:novel:book_name"),
        )

    def get_chapter_page(self):
        res = self.request(get, f"/book/{self.book.book_id}.html")
        for item in res.css("html body div.wrap div.con div.chapterList div.page2.font12 span.selectW.chapter_page select.select option").getall():
            yield self.parse_html(item).css("option").attrib.get("value")

    def get_chapter_list(self, page_index, _book_data: BookData):
        res = self.request(post, '/index.php?action=loadChapterPage', data={
            'id': self.book.book_id,
            'page': page_index,
        }).json()
        for chapter in res.get('data', []):
            yield ChapterModel.from_dict(chapter)

    def get_chapter_content(self, chapter: ChapterModel) -> ChapterModel:
        res = self.request(get, chapter.url)
        content = self.markdown(res.css("#content p").getall())
        chapter.content = content
        return chapter

    def search_book(self, keyword: str):
        pass
