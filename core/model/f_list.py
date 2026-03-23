class FList:
    __data = []

    def __init__(self, data=None):
        if data is None:
            data = []
        self.__data = data

    def __add__(self, other):
        self.__data.append(other)
        return self

    def __index__(self, index):
        return self.__data[index]

    def __len__(self):
        return len(self.__data)

    def filter(self, key, value):
        return FList([item for item in self.__data if getattr(item, key) == value])

    def __iter__(self):
        return iter(self.__data)

    def __str__(self):
        _str = "[\n"
        for item in self.__data:
            _str += f"  {item}\n"
        _str += "]"
        return _str