ostruct
=======

[![Package Status](http://img.shields.io/pypi/v/ostruct.svg)](https://pypi.python.org/pypi/ostruct)
[![Build Status](https://travis-ci.org/hamidnazari/python-ostruct.svg?branch=master)](https://travis-ci.org/hamidnazari/python-ostruct)

OpenStruct for Python.

```python
from ostruct import OpenStruct

car = OpenStruct()
car.make = 'Ford'
car.model = 'Mustang'
car.owner.name = 'John Doe'
car.owner.age = 30

print car # {'owner': {'age': 30, 'name': 'John Doe'}, 'make': 'Ford', 'model': 'Mustang'}
```

Install
-------
```
$ pip install ostruct
```
