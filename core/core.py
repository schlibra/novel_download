import os
import yaml
from core.adapter import Adapter
from adapter.shuyoushe import ShuYouSheAdapter


class Core:
    book_list = []
    @staticmethod
    def make_dirs():
        os.makedirs('books', exist_ok=True)
    @staticmethod
    def get_adapter(site_name):
        return {
            'shuyoushe': ShuYouSheAdapter
        }.get(site_name, Adapter)
    def load_books(self, file_path='list.yml'):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")
        with open(file_path, 'r', encoding='utf-8') as f:
            self.book_list = yaml.load(f, Loader=yaml.FullLoader)
        return self
    def get_books(self):
        for book in self.book_list:
            if book.get('skip', False):
                continue
            book_url = book.get('url', '')
            site = book.get('site', '')
            adapter = self.get_adapter(site)(book_url)
            book_info = adapter.get_book_info()
            if book_info:
                book_name = book_info.get('book_name', '')
                print(f'Downloading {book_name}')
                book_author = book_info.get('book_author', '')
                book_desc = book_info.get('book_desc', '')
                total_chapters = book_info.get('total_chapters', 0)
                _count_length = len(str(total_chapters))
                book_dir = os.path.join('books', book_name)
                metadata_dir = os.path.join(book_dir,'metadata')
                chapters_dir = os.path.join(book_dir, 'chapters')
                os.makedirs(book_dir, exist_ok=True)
                os.makedirs(metadata_dir, exist_ok=True)
                os.makedirs(chapters_dir, exist_ok=True)
                open(os.path.join(metadata_dir, 'book_name.txt'), 'w', encoding='utf-8').write(book_name)
                open(os.path.join(metadata_dir, 'book_author.txt'), 'w', encoding='utf-8').write(book_author)
                open(os.path.join(metadata_dir, 'book_desc.txt'), 'w', encoding='utf-8').write(book_desc)
                open(os.path.join(metadata_dir, 'total_chapters.txt'), 'w', encoding='utf-8').write(str(total_chapters))
                open(os.path.join(metadata_dir, 'site.txt'), 'w', encoding='utf-8').write(site)
                open(os.path.join(metadata_dir, 'book_url.txt'), 'w', encoding='utf-8').write(book_url)
                for num in range(1, total_chapters+1):
                    print(f'Getting chapter {num} content')
                    chapter = adapter.get_chapter_content(num)
                    chapter_title = chapter.get('chapter_title', '')
                    print(f'Chapter {num} {chapter_title}')
                    chapter_content = chapter.get('chapter_content', '')
                    page_index = str(num).zfill(_count_length)
                    chapter_file = os.path.join(chapters_dir, f'{page_index}_{chapter_title}.txt')
                    open(chapter_file, 'w', encoding='utf-8').write(chapter_content)
                    print(f'Saved chapter {page_index} {chapter_title}')
            else:
                raise ValueError(f"Failed to get book info from {book_url}")

