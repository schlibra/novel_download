from core.adapter.Bqg475 import Bqg475Adapter
from core.model import BookInfo


def search():
    print(Bqg475Adapter(BookInfo()).search_book("斗罗大陆").filter('author', '唐家三少'))

if __name__ == '__main__':
    search()