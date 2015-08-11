class OpenStruct(dict):
    """OpenStruct, the flexible data structure."""
    def __init__(self, clone=None, **kwargs):
        super(OpenStruct, self).__init__()

        if isinstance(clone, OpenStruct):
            kwargs.update(**clone.__dict__)
        elif isinstance(clone, dict):
            kwargs.update(**clone)

        for key, value in kwargs.items():
            self.__dict__[key] = self.__convert(value)

    def iteritems(self):
        try:
            return self.__dict__.iteritems()
        except AttributeError:
            return self.__dict__.items()

    def items(self):
        return self.iteritems()

    def __convert(self, value):
        if isinstance(value, (list, tuple)):
            dictionary = []
            for item in value:
                dictionary.append(self.__convert(item))
            return dictionary
        elif isinstance(value, OpenStruct):
            return OpenStruct(**value.__dict__)
        elif isinstance(value, dict):
            return OpenStruct(**value)
        else:
            return value

    def __getattr__(self, key):
        if not self.__dict__.get(key):
            self.__dict__[key] = OpenStruct()

        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):
        return str(self.__dict__)

    def __cmp__(self, rhs):
        raise TypeError('unorderable types')

    def __lt__(self, rhs):
        raise TypeError('unorderable types')

    def __gt__(self, rhs):
        raise TypeError('unorderable types')

    def __le__(self, rhs):
        raise TypeError('unorderable types')

    def __ge__(self, rhs):
        raise TypeError('unorderable types')

    def __eq__(self, rhs):
        if hasattr(rhs, '__dict__'):
            return self.__dict__ == rhs.__dict__

        return self.__dict__ == rhs

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    def __len__(self):
        return len(self.__dict__)
