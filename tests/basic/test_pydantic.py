import pytest
from typing import List, Union, Optional
from pydantic import BaseModel, validator, validate_arguments, ValidationError, constr


class Times(BaseModel):
    # org: int
    org: Union[str, List[Union[int, float]]]


def times(org):
    return Times(org=org)


def test_01():
    # t = Times(org="a")
    # t = Times(org=[1, 1.5, True])
    t = times([1])


class IntOrFloat(BaseModel):
    val: float


def test_02():
    """自動キャスト
    pydanticは可能ならキャストしてくれる
    型をintとしていれば、strの"1"を渡しても
    キャストしてくれる
    なのでint or floatの場合はfloat型に
    しておけばOK
    """
    i = IntOrFloat(val=2)
    assert i.val == 2
    assert type(i.val) is float
    i = IntOrFloat(val=2.1)
    assert i.val == 2.1


class TextOrNumber(BaseModel):
    text: Optional[str]
    val: Optional[float]
    check: bool = True

    @validator("*")
    def validate_text(cls, v, values):
        print("v,values:=============== ", v, values)
        if values.get("text"):
            return values["text"]
        elif v:
            return v
        raise ValueError("text,valのどちらかに値が必要です")


@validate_arguments
def culc(a: int, b: int):
    return a + b


def test03():
    assert culc(1, 2) == 3
    assert culc("1", "2") == 3  # 1,2にcast
    assert culc(True, False) == 1  # 1,0にcast
    with pytest.raises(ValidationError) as e:
        culc("hello", ["world"])
    assert "'loc': ('a',), 'msg': 'value is not a valid integer'" in str(e)
    assert "'loc': ('b',), 'msg': 'value is not a valid integer'" in str(e)


@validate_arguments
def reg_str(s: constr(strip_whitespace=True, regex=r"^\d{2}:\d{2}:\d{2}$")):
    return s


def test04():
    """正規表現にマッチしないとエラー"""
    assert reg_str("00:00:01") == "00:00:01"
    assert reg_str("  00:00:01 ") == "00:00:01"  # strip_whitespaceによりトリムする
    with pytest.raises(ValidationError) as e:
        reg_str("0:0:1")  # 正規表現にマッチしないのでエラー
    assert "string does not match regex" in str(e)
