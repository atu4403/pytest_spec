# pytest_spec

pytestの使用法を実際のtestを行った上でまとめています。  
ハマるポイントや何回も調べ直すことを中心にしているので基本的な使用法には触れていません。

## 環境
- macOS 10.14.6
- Python 3.8.6
- pytest (5.4.3)
- pytest-cov (2.10.1)
- pytest-mock (3.3.1)
- pytest-watch (4.2.0)

---

### 例外のtest

```python
def division_by_zero(n: int):
    """ゼロで割る関数"""
    ans = n / 0
    return ans
```

```python
def test_zero(parameter_list):
    with pytest.raises(ZeroDivisionError) as e:
        basic.division_by_zero(1)
    assert e.type == ZeroDivisionError
    assert e.typename == "ZeroDivisionError"
    assert str(e.value) == "division by zero"
```

ポイントはwith文の中で例外が発生したらその後の処理は行われないという所。アサーションはwithの外に置く。

---

### 無限ループのtest

```python
def hello(name: str = "world"):
    print(f"hello {name}!!")
    return


def loop_define(val: any):
    return val


def loop_sample_define():
    while loop_define(1):
        hello("loop")
```
関数`loop_sample_define`は無限に`hello loop!!`を出力する。whileの条件判定を関数に置き換えてそれをmockにすることでループを止める事ができる。


```python
import src.pytest_spec.basic as basic
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
```

`loop_sample_define`の中で使われている`loop_define`をmock化する。引数`side_effect`を設定する事により3回目のwhileでfalseとなり処理が止まる。なので3回目の`hello`は呼ばれない。  
また、`side_effect`による引数はあくまでmockが書き換えているだけである。表面上`loop_define`は引数1で呼んでいるので`mock_calls`には表面上の引数が記録される。
---

### クラスインスタンスのtest

```python
import sched
import time

def hello(name: str = "world"):
    print(f"hello {name}!!")
    return

def inner_instance_sample():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(60, 1, hello)
    s.run()

```

`sched.scheduler`インスタンスを返す。このインスタンス`s`に対し`enter`と`run`のメソッドが呼ばれたかtestを行う。

```python
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
```

インスタンスをモックにする方法は3つ。まず下準備として`mocker.patch("sched.scheduler")`としてschedulerクラスをモック化する。  
このモック(関数)を呼び出すと返り値はインスタンスのモックになる。

1. sched.scheduler()
2. scheduler_mock()
3. scheduler_instance

上記の例では、この3つは全く同じものを参照している同一のモックである。