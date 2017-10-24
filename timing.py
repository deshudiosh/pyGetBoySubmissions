import atexit
from datetime import timedelta
from time import time, strftime, localtime

timing_start = 0

def _secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))

def _log(s, elapsed=None):
    line = "="*40
    print(line)
    print(_secondsToStr(), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def _endlog():
    end = time()
    elapsed = end-timing_start
    _log("End Program", _secondsToStr(elapsed))


def init():
    global timing_start
    timing_start = time()
    atexit.register(_endlog)
    _log("Start Program")