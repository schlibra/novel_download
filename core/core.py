import os

import yaml

from .base_adapter import Adapter
from .adapter import *
from .model import *


class Core:
    base_path = 'books'
    @staticmethod
    def load_book_list(list_file_path: str='list.yml'):
        if os.path.exists(list_file_path):
            book_list = yaml.load(open(list_file_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
            for book in book_list:
                yield BookInfo.from_dict(book)
        else:
            raise FileNotFoundError(f"File {list_file_path} not found.")

    @staticmethod
    def get_adapter(book: BookInfo):
        return {
            'shuyoushe': ShuYouSheAdapter,
            'bqg475': Bqg475Adapter
        }.get(book.site, Adapter)(book)

    @staticmethod
    def mkdir(path: str):
        print(f"mkdir {path}")
        os.makedirs(path, exist_ok=True)

    def write_book_data(self, _book_data: BookData):
        self.mkdir(self.base_path)
        book_path = os.path.join(self.base_path, _book_data.book_name)
        self.mkdir(book_path)
        metadata_path = os.path.join(book_path,'metadata')
        chapters_path = os.path.join(book_path, 'chapters')
        self.mkdir(metadata_path)
        self.mkdir(chapters_path)
        with open(os.path.join(metadata_path, 'description.txt'), 'w', encoding='utf-8') as f:
            f.write(_book_data.description)
        with open(os.path.join(metadata_path, 'author.txt'), 'w', encoding='utf-8') as f:
            f.write(_book_data.author)
        with open(os.path.join(metadata_path, 'book_url.txt'), 'w', encoding='utf-8') as f:
            f.write(_book_data.book_url)
        with open(os.path.join(metadata_path, 'book_name.txt'), 'w', encoding='utf-8') as f:
            f.write(_book_data.book_name)

    def write_chapter_data(self, chapter_data: ChapterModel):
        chapter_data_path = os.path.join(self.base_path, chapter_data.book_name, 'chapters', f"{chapter_data.order}_{chapter_data.title}.txt")
        with open(chapter_data_path, 'w', encoding='utf-8') as f:
            f.write(chapter_data.content)

    def run(self):
        for book in self.load_book_list():
            if not book.skip:
                adapter = self.get_adapter(book)
                print(f"Downloading {book.book_id} adapter {adapter.adapter_name}")
                _book_data = adapter.get_book_data()
                print(f"Book data: {_book_data}")
                self.write_book_data(_book_data)
                for page in adapter.get_chapter_page():
                    print(f"Downloading page {page}")
                    for chapter in adapter.get_chapter_list(page, _book_data):
                        print(f"Downloading chapter {chapter}")
                        chapter_data = adapter.get_chapter_content(chapter)
                        self.write_chapter_data(chapter_data)
                        print(f"Downloaded chapter {chapter.title}")
                exit()