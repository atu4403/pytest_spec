import pytest
import src.pytest_spec.basic as basic


class TestErrors:
    def test_zero(parameter_list):
        with pytest.raises(ZeroDivisionError) as e:
            basic.division_by_zero(1)
        assert e.type == ZeroDivisionError
        assert e.typename == "ZeroDivisionError"
        assert str(e.value) == "division by zero"
