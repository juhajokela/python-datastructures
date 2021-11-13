# Python Datastructures

I'm just here fooling around with funny ideas of different datastructures, nothing serious really.

### BiDict

Datastructure that works like map or dict (in python), but is bi-directional.

```

```

### MultiBiDict

...

### Array

Python list-like datastructure that supports map and filter methods.

``` python
>>> Array(1,2,3)
Array(1, 2, 3)
>>> array = _
>>> array.map(lambda x: x*3)
Array(3, 6, 9)
>>> array.filter(lambda x: x != 2)
Array(1, 3)
```

### Map

Python dict-like datastructure that supports map and filter methods.

``` python
>>> Map({'a': 1, 'b': 2})
Map('a': 1, 'b': 2)
>>> map = _
>>> map.map(lambda k, v: (k+'x', v*3))
Map('bx': 6, 'ax': 3)
>>> map.filter(lambda k, v: k != 'a' and v != 2)
Map()
```
