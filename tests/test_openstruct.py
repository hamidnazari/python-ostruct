import pytest
from ostruct import OpenStruct
import pickle


def test_empty_struct():
    o = OpenStruct()

    assert o == {}
    assert isinstance(o, OpenStruct)
    assert isinstance(o.__dict__, dict)

    if o:
        assert False
    else:
        assert True

    if not o:
        assert True
    else:
        assert False


def test_booleans():
    o = OpenStruct(true=True, false=False)

    assert o.true is True
    assert o.false is False
    assert o['true'] is True
    assert o['false'] is False
    assert isinstance(o.none, OpenStruct)


def test_shallow_struct():
    o = OpenStruct()
    o.a = 10

    assert o.a == 10
    assert o.nonexistent_attribute is not None

    if o:
        assert True
    else:
        assert False

    if not o:
        assert False
    else:
        assert True


def test_nested_struct():
    o = OpenStruct()
    o.a.b.c.d = 10

    assert o.a.b.c.d == 10
    assert o.a.b.c == {'d': 10}
    assert o.a.b == {'c': {'d': 10}}
    assert o.a == {'b': {'c': {'d': 10}}}
    assert o == {'a': {'b': {'c': {'d': 10}}}}


def test_constructor_clone():
    o = OpenStruct(a=1, b=2, c=4)
    assert o == {'a': 1, 'b': 2, 'c': 4}

    a = OpenStruct(o)
    assert o == a

    b = OpenStruct(o.__dict__)
    assert o == b

    c = OpenStruct(**(o.__dict__))
    assert o == c

    d = OpenStruct(**o)
    assert o == d


@pytest.mark.parametrize("kwargs,expected,expected2", [
    ({}, "{}", None),

    ({'a': 1}, "{'a': 1}", None),

    ({'a': 1, 'b': 'Hello'},
     "{'a': 1, 'b': 'Hello'}",
     "{'b': 'Hello', 'a': 1}"),

    ({'a': 1, 'b': {'b1': 1e100}},
     "{'a': 1, 'b': {'b1': 1e+100}}",
     "{'b': {'b1': 1e+100}, 'a': 1}"),
])
def test__repr(kwargs, expected, expected2):
    o = OpenStruct(**kwargs)
    assert str(o) == expected or str(o) == expected2


@pytest.mark.parametrize("value,expected", [
    (1, 1),
    ('Hello', 'Hello'),
    ((), ()),
    ((1, 2), (1, 2)),
    (('Hello', 'World'), ('Hello', 'World')),
    ([], []),
    ([1, 2], [1, 2]),
    (['Hello', 'World'], ['Hello', 'World']),
    ({'a': 1, 'b': 2}, OpenStruct({'a': 1, 'b': 2})),
    (({'a': 1, 'b': 2}, {'c': 3}), ({'a': 1, 'b': 2}, {'c': 3})),
    ([{'a': 1, 'b': 2}, {'c': 3}], [{'a': 1, 'b': 2}, {'c': 3}]),
    (OpenStruct({'a': 1, 'b': 2}), OpenStruct({'a': 1, 'b': 2})),
    ((OpenStruct({'a': 1, 'b': 2})), (OpenStruct({'a': 1, 'b': 2}))),
    ([OpenStruct({'a': 1, 'b': 2})], [OpenStruct({'a': 1, 'b': 2})]),
])
def test_convert(value, expected):
    assert OpenStruct._convert(value) == expected


@pytest.mark.parametrize("value", [
    1,
    1.2,
    (1, 2, 3),
    [{'a': 1, 'b': 2, 'c': 4}],
    'Hello',
    lambda x: x**2
])
def test_constructor_bad_args(value):
    with pytest.raises(TypeError):
        OpenStruct(value)


def test_comparisons():
    o1 = OpenStruct()
    o1.a.b.c = 10

    assert (o1 == 10) is False
    assert (o1 is True) is False

    o2 = OpenStruct()
    o2.a.b.c = 10

    assert (o1 == o2) is True
    assert (o1 != o2) is False
    assert (o1 is o2) is False
    assert (o2 is o1) is False

    with pytest.raises(TypeError):
        o1 > o2

    with pytest.raises(TypeError):
        o1 < o2

    with pytest.raises(TypeError):
        o1 >= o2

    with pytest.raises(TypeError):
        o1 <= o2


def test_iter():
    keys = []
    o = OpenStruct(a=1, b=2, c=4, d=8)

    for key in o:
        keys.append(key)

    assert sorted(keys) == sorted(['a', 'b', 'c', 'd'])


def test_iteritems():
    s = 0
    o = OpenStruct(a=1, b=2, c=4, d=8)

    for key, value in o.iteritems():
        s += value

    assert s == 15


def test_items():
    s = 0
    o = OpenStruct(a=1, b=2, c=4, d=8)

    for key, value in o.items():
        s += value

    assert s == 15


def test_keys():
    o = OpenStruct()
    assert len(o.keys()) == 0

    o = OpenStruct(a=1, b=2, c=4)
    assert sorted(o.keys()) == sorted(['a', 'b', 'c'])


def test_set_get_item():
    o = OpenStruct()
    o['a'] = 10
    assert o['a'] == 10
    assert o.a == 10

    o = OpenStruct()
    o['a']['b']['c'] = 10
    assert o['a']['b']['c'] == 10
    assert o['a']['b'] == {'c': 10}
    assert o['a'] == {'b': {'c': 10}}
    assert o == {'a': {'b': {'c': 10}}}


def test_delete_attr():
    o = OpenStruct(a=1, b=2, c=4)

    del o.b
    assert o == {'a': 1, 'c': 4}

    o.b.d.e = 10

    del o.b.d
    assert o == {'a': 1, 'c': 4, 'b': {}}

    del o
    with pytest.raises(NameError):
        assert o  # NoQA


def test_delete_item():
    o = OpenStruct(a=1, b=2, c=4)

    del o['b']
    assert o == {'a': 1, 'c': 4}

    o.b.d.e = 10

    del o['b']['d']
    assert o == {'a': 1, 'c': 4, 'b': {}}


@pytest.mark.parametrize("value,expected", [
    (None, 0),
    ({'a': 1, 'b': 2, 'c': 4}, 3),
    (OpenStruct(a=1, b=2, c=4, d=8), 4),
])
def test_len(value, expected):
    o = OpenStruct(value)
    assert len(o) == expected


def test_types():
    d = {'a': 1, 'b': 2, 'c': 3}

    o = OpenStruct(
        a=d,
        b=OpenStruct(d)
    )
    o.n.o = 1
    o.p = d
    o.q = OpenStruct(d)

    assert isinstance(o, OpenStruct)
    assert isinstance(o.a, dict)
    assert isinstance(o.b, OpenStruct)
    assert isinstance(o.n, OpenStruct)
    assert isinstance(o.n.o, int)
    assert isinstance(o.p, dict)
    assert isinstance(o.q, OpenStruct)


def test_inheritance_types():
    class TestOpenStruct(OpenStruct):
        pass

    class AnotherOpenStruct(OpenStruct):
        pass

    d = {'a': 1, 'b': 2, 'c': 3}

    o = TestOpenStruct(
        a=d,
        b=OpenStruct(d),
        c=TestOpenStruct(d),
        d=AnotherOpenStruct(d),
        e=TestOpenStruct(AnotherOpenStruct(d))
    )
    o.n.o = 1
    o.p = d
    o.q = OpenStruct(d)
    o.r = TestOpenStruct(d)
    o.s = AnotherOpenStruct(d)
    o.t = TestOpenStruct(AnotherOpenStruct(d))

    assert isinstance(o, TestOpenStruct)
    assert isinstance(o.a, dict)
    assert not isinstance(o.b, TestOpenStruct)
    assert isinstance(o.c, TestOpenStruct)
    assert isinstance(o.d, AnotherOpenStruct)
    assert isinstance(o.e, TestOpenStruct)
    assert isinstance(o.n, TestOpenStruct)
    assert isinstance(o.n.o, int)
    assert isinstance(o.p, dict)
    assert not isinstance(o.q, TestOpenStruct)
    assert isinstance(o.r, TestOpenStruct)
    assert isinstance(o.s, AnotherOpenStruct)
    assert isinstance(o.t, TestOpenStruct)


@pytest.mark.parametrize("struct", [
    (OpenStruct(A=1, B=2, C=3)),
    (OpenStruct(A=1, B=2, C=[1, 2, 3, 4])),
    (OpenStruct(A=1, B=2, C=[1, 2, [3, 4]])),
    (OpenStruct(A=1, B=2, C=OpenStruct(x=1, y=2))),
    (OpenStruct(A="string1", B="string2",
                C=OpenStruct(AA=OpenStruct(AAA=1, BBB="inception"))))
])
def test_pickling(struct):
    bin = pickle.dumps(struct)
    loaded = pickle.loads(bin)
    assert struct == loaded
