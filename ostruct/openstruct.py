from collections.abc import MutableMapping


class OpenStruct(MutableMapping):
    """OpenStruct, the flexible data structure."""
    def __init__(self, clone=None, dict_convert=False, **kwargs):
        super(OpenStruct, self).__init__()

        if isinstance(clone, OpenStruct):
            kwargs.update(**clone.__dict__)
        elif isinstance(clone, dict):
            kwargs.update(**clone)
        elif clone is not None:
            raise TypeError('Type to be cloned is not supported.')

        for key, value in kwargs.items():
            self.__dict__[key] = self._convert(value, dict_convert)

    @classmethod
    def _convert(cls, value, dict_convert=False):
        if dict_convert and isinstance(value, dict):
            return cls(**value)
        elif isinstance(value, (list, tuple)):
            dictionaries = []
            for item in value:
                dictionaries.append(cls._convert(item, dict_convert))

            if isinstance(value, tuple):
                dictionaries = tuple(dictionaries)

            return dictionaries
        elif isinstance(value, OpenStruct):
            return value.__class__(**value)
        else:
            return value

    def iteritems(self):
        try:
            return self.__dict__.iteritems()
        except AttributeError:
            return self.__dict__.items()

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def __iter__(self):
        return self.__dict__.__iter__()

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    def __delitem__(self, key):
        self.__dict__.__delitem__(key)

    def __getattr__(self, key):
        if self.__dict__.get(key) is None:
            self.__dict__[key] = self.__class__()

        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __delattr__(self, key):
        self.__dict__.pop(key, None)

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
