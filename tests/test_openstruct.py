from ostruct import OpenStruct


def test_empty_struct():
    o = OpenStruct()

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


def test_shallow_struct():
    o = OpenStruct()
    o.a = 10

    assert o.a == 10

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


def test_comparisons():
    o1 = OpenStruct()
    o1.a.b.c = 10

    assert (o1 == 10) is False
    assert (o1 is True) is False

    o2 = OpenStruct()
    o2.a.b.c = 10

    assert (o1 == o2) is True
    assert (o1 != o2) is False
    assert (o1 > o2) is False
    assert (o1 >= o2) is True
    assert (o1 <= o2) is True
    assert (o1 is o2) is False
    assert (o2 is o1) is False


def test_iteritems():
    o = OpenStruct()

    o.a = 1
    o.b = 2
    o.c = 4
    o.d = 8

    s = 0

    for key, value in o.iteritems():
        s += value

    assert s == 15
