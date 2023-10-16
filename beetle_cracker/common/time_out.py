#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
    return {}


def callback_func(e):
    print('run func timeout')
    return {}


def time_out_gevent(interval, callback=None):
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
                return callback(e) if callback else None

        return wrapper

    return decorator
