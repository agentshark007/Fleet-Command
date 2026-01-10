import time
import sys
import inspect

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"


def _caller_file():
    frame = inspect.stack()[2]
    return frame.filename.split("/")[-1]


def _timestamp():
    t = time.time()
    lt = time.localtime(t)
    ms = int((t - int(t)) * 1000)
    return time.strftime("%H:%M:%S", lt) + f".{ms:03d}"


def _log(color, level, message):
    file = _caller_file()
    ts = _timestamp()
    print(f"{color}{ts} [{level:<5}] ({file}) {RESET}{message}", file=sys.stdout)


def info(message):
    _log(GREEN, "INFO", message)


def warn(message):
    _log(YELLOW, "WARN", message)


def fatal(message):
    _log(RED, "FATAL", message)
