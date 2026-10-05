from collections.abc import MutableMapping
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union


class OpenStruct(MutableMapping):
    """OpenStruct, the flexible data structure."""

    def __init__(self, clone: Any = None, dict_convert: bool = False, **kwargs: Any) -> None:
        super().__init__()

        if isinstance(clone, OpenStruct):
            kwargs.update(**clone.__dict__)
        elif isinstance(clone, dict):
            kwargs.update(**clone)
        elif clone is not None:
            raise TypeError('Type to be cloned is not supported.')

        for key, value in kwargs.items():
            self.__dict__[key] = self._convert(value, dict_convert)

    @classmethod
    def _convert(cls, value: Any, dict_convert: bool = False) -> Any:
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

    def to_dict(self) -> Dict[str, Any]:
        """Recursively convert OpenStruct and nested OpenStructs to standard Python dicts."""
        result: Dict[str, Any] = {}
        for key, value in self.__dict__.items():
            result[key] = self._to_dict_item(value)
        return result

    @classmethod
    def _to_dict_item(cls, value: Any) -> Any:
        if isinstance(value, OpenStruct):
            return value.to_dict()
        elif isinstance(value, list):
            return [cls._to_dict_item(item) for item in value]
        elif isinstance(value, tuple):
            return tuple(cls._to_dict_item(item) for item in value)
        elif isinstance(value, dict):
            return {k: cls._to_dict_item(v) for k, v in value.items()}
        else:
            return value

    def items(self) -> Any:
        return self.__dict__.items()

    def keys(self) -> Any:
        return self.__dict__.keys()

    def __iter__(self) -> Iterator[str]:
        return self.__dict__.__iter__()

    def __setitem__(self, key: str, value: Any) -> None:
        self.__setattr__(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.__getattr__(key)

    def __getstate__(self) -> Dict[str, Any]:
        return self.__dict__

    def __setstate__(self, d: Dict[str, Any]) -> None:
        self.__dict__.update(d)

    def __delitem__(self, key: str) -> None:
        self.__dict__.__delitem__(key)

    def __getattr__(self, key: str) -> Any:
        if key.startswith('__') and key.endswith('__'):
            return super().__getattr__(key)

        if self.__dict__.get(key) is None:
            self.__dict__[key] = self.__class__()

        return self.__dict__[key]

    def __setattr__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delattr__(self, key: str) -> None:
        self.__dict__.pop(key, None)

    def __dir__(self) -> List[str]:
        return list(set(super().__dir__()) | set(self.__dict__.keys()))

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __lt__(self, rhs: Any) -> Any:
        raise TypeError('unorderable types')

    def __gt__(self, rhs: Any) -> Any:
        raise TypeError('unorderable types')

    def __le__(self, rhs: Any) -> Any:
        raise TypeError('unorderable types')

    def __ge__(self, rhs: Any) -> Any:
        raise TypeError('unorderable types')

    def __eq__(self, rhs: Any) -> bool:
        if hasattr(rhs, '__dict__'):
            return self.__dict__ == rhs.__dict__

        return self.__dict__ == rhs

    def __ne__(self, rhs: Any) -> bool:
        return not self.__eq__(rhs)

    def __len__(self) -> int:
        return len(self.__dict__)
