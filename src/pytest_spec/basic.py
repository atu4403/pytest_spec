import sched
import time


class MyError(Exception):
    """自作のエラークラス"""

    pass


def division_by_zero(n: int):
    """ゼロで割る関数"""
    ans = n / 0
    return ans


def hello(name: str = "world"):
    print(f"hello {name}!!")
    return


def loop_define(val: any):
    return val


def loop_sample_define():
    while loop_define(1):
        hello("loop")


class LoopSample(object):
    """
    TODO: test未作成
    """

    @staticmethod
    def loop_define(val: any):
        return val

    def loop_sample_define():
        while loop_define(1):
            hello("loop")


def inner_instance_sample():
    s = sched.scheduler(time.time, time.sleep)
    s.enter(60, 1, hello)
    s.run()
