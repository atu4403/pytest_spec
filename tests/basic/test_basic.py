import pytest
import pytest_spec.basic as basic


class TestErrors:
    def test_zero(parameter_list):
        with pytest.raises(ZeroDivisionError) as e:
            basic.division_by_zero(1)
        assert e.type == ZeroDivisionError
        assert e.typename == "ZeroDivisionError"
        assert str(e.value) == "division by zero"


# 引数を変えて行うtest
def add(a, b):
    if type(a) is not int or type(b) is not int:
        raise TypeError
    return a + b


@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (4, 5, 9), (10, 23, 33)])
def test_add(a, b, expected):
    assert add(a, b) == expected


# 引数を変えて、いずれも例外を吐くことを確認するtest
@pytest.mark.parametrize("a,b,expected", [("1", 2, 3), (None, 5, 9), (10, [1], 33)])
def test_add_2(a, b, expected):
    with pytest.raises(TypeError):
        add(a, b)
