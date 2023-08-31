# 一些练习思考的case
import os,sys
import dis

# python frame
# type: ignore [no-redef]
import inspect
# reference https://github.com/gaogaotiantian/objprint
from objprint import op

def f3():
    frame = inspect.currentframe()
    op(
        frame,
        honor_existing=False,
        depth=1
    )
    op(
        frame.f_code.co_code,
        honor_existing=False,
        depth=1
    )
    op(frame.f_code.co_name)

f3()
# 保存每一次的测试代码，新代码提前退出，保证后面代码不执行
sys.exit(0)

from typing import Optional, Any, NoReturn, Callable, Literal

def my_dec(func: Callable[[int,int],int]):
    def wrapper(a: int, b:int) -> int:
        print(f"args:{a} {b}")
        ret = func(a, b)
        print(f"result: {ret}")
        return ret
    return wrapper

@my_dec
def f0(a:int, b:int) -> int:
    return a + b

def f1(a: Any) -> Any:
    return a

def f(x: Optional[int]) -> int:
    if x is None:
        return 0
    return x
import subprocess


print(f(None))
# print(f('a'))

os._exit(0)

# staticmethod与classmethod


class A:
    @staticmethod
    def f(x):
        print(x)

    @classmethod
    def g(cls, x):
        print(x)


print(A.f)
dis.dis(A.f)

os._exit(0)


# class中定义的函数怎么执行

class A1:
    def f(self, data):
        print('A.f running')
        print(data)


o = A1()
o.f("data arg")

A1.f(o, "data arg 2")
