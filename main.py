from core import Core


def main():
    Core().load_books().get_books()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('用户终止程序')
    # except Exception as e:
    #     print('程序出错：', e)