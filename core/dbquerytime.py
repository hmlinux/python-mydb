#/usr/bin/env python3
# _*_ coding: utf-8 _*_
import time

def sql_querytime(func):
    def wapper(*args, **kargs):
        start_time = time.time()
        query_result = func(*args, **kargs)
        stop_time = time.time()
        end_time = stop_time - start_time
        if query_result == True:
            print("(%.4f sec)" % end_time)
    return wapper