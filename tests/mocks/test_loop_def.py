import pytest_spec.basic as basic
from pytest_mock import mocker


def test_loop_define(mocker):
    mocker.patch.object(basic, "loop_define", side_effect=[2, 3, 0])
    mocker.patch.object(basic, "hello")
    basic.loop_sample_define()
    basic.loop_define.assert_any_call(1)
    assert len(basic.loop_define.mock_calls) == 3
    assert len(basic.hello.mock_calls) == 2
    assert basic.loop_define.mock_calls == [
        mocker.call(1),
        mocker.call(1),
        mocker.call(1),
    ]
