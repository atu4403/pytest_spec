import sched
import pytest_spec.basic as basic
from pytest_mock import mocker


def test_instance_mock(mocker):
    scheduler_mock = mocker.patch("sched.scheduler")
    scheduler_instance = scheduler_mock.return_value
    basic.inner_instance_sample()
    assert scheduler_mock().run is sched.scheduler().run
    assert scheduler_mock().run is scheduler_instance.run
    scheduler_mock().enter.assert_called_once_with(60, 1, basic.hello)
    scheduler_mock().run.assert_called_once_with()
    scheduler_instance.run.assert_called_once_with()
