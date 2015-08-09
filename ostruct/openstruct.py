class OpenStruct(dict):
    """OpenStruct, the flexible data structure."""
    def __init__(self, **kwargs):
        super(OpenStruct, self).__init__()

        for key, value in kwargs.items():
            self.__dict__[key] = self.__convert(value)

    def __getattr__(self, key):
        if not self.__dict__.get(key):
            self.__dict__[key] = OpenStruct()

        return self.__dict__[key]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __repr__(self):
        return str(self.__dict__)

    def __convert(self, value):
        if isinstance(value, (list, tuple)):
            dictionary = []
            for item in value:
                dictionary.append(self.__convert(item))
            return dictionary
        elif isinstance(value, dict):
            return OpenStruct(**value)
        else:
            return value
