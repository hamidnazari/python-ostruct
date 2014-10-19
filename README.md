ostruct
=======

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
