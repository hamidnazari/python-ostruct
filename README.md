ostruct
=======

[![PyPI](https://img.shields.io/pypi/v/ostruct.svg)](https://pypi.org/project/ostruct/)
[![CI](https://github.com/hamidnazari/python-ostruct/actions/workflows/qa.yml/badge.svg)](https://github.com/hamidnazari/python-ostruct/actions/workflows/qa.yml)
[![Release](https://github.com/hamidnazari/python-ostruct/actions/workflows/release.yml/badge.svg)](https://github.com/hamidnazari/python-ostruct/actions/workflows/release.yml)

OpenStruct for Python.

```python
from ostruct import OpenStruct

car = OpenStruct()
car.make = 'Ford'
car.model = 'Mustang'
car.owner.name = 'John Doe'
car.owner.age = 30

print(car) # {'owner': {'age': 30, 'name': 'John Doe'}, 'make': 'Ford', 'model': 'Mustang'}
```

Install
-------

```sh
python -m pip install ostruct
```

**Note:** the latest version to support Python 2.7 is `ostruct==3.0.1`.

Development
-----------

```sh
python -m pip install --editable ".[test,dev]"
make lint test package
```
