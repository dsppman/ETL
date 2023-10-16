#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import signal


# 自定义超时异常
class TimeoutError(Exception):
    def __init__(self, msg):
        super(TimeoutError, self).__init__()
        self.msg = msg


def time_out(interval, callback):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError("run func timeout")

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)  # interval秒后向进程发送SIGALRM信号
                result = func(*args, **kwargs)
                signal.alarm(0)  # 函数在规定时间执行完后关闭alarm闹钟
                return result
            except TimeoutError as e:
                result = callback(e)
                return result

        return wrapper

    return decorator


def timeout_callback(e):
    print(e.msg)
    return 0, 1


@time_out(2, timeout_callback)
def task1():
    print("task1 start")
    time.sleep(300)
    print("task1 end")
    return 1, 1


@time_out(2, timeout_callback)
def task2():
    print("task2 start")
    time.sleep(1)
    print("task2 end")
    return 2, 1


def callback_func():
    print('run func timeout')
    return {}, 0


def time_out(interval, callback=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            ########## 该部分必选在requests之前导入
            import gevent
            from gevent import monkey
            monkey.patch_all()
            ##########

            try:
                return gevent.with_timeout(interval, func, *args, **kwargs)
            except gevent.timeout.Timeout as e:
                return callback() if callback else None

        return wrapper

    return decorator


@time_out(3, callback_func)
def func(a, b):
    import time
    time.sleep(2)
    return a, b


if __name__ == "__main__":
    a, b = func(1, 2)
    c = 1
    # res,exist = task1()
    # print("res:{}".format(res))
    # res,exist = task2()
    # print("res:{}".format(res))
