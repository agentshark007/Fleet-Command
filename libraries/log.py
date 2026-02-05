import time
_log_file = None
_log_level = 20
_console = True
_GREEN = '\x1b[32m'
_YELLOW = '\x1b[33m'
_RED = '\x1b[31m'
_CYAN = '\x1b[36m'
_RESET = '\x1b[0m'
_LEVELS = {'DEBUG': 10, 'INFO': 20, 'WARN': 30, 'ERROR': 40, 'FATAL': 50}


def reset(file: str = 'app.log', level: str = 'INFO', console: bool = True):
    global _log_file, _log_level, _console
    _log_file = file
    _log_level = _LEVELS.get(level.upper(), 20)
    _console = console
    with open(_log_file, 'w') as f:
        f.write(f'Log Started with level: {level}\n')


def debug(message: str):
    _log('DEBUG', message, _CYAN)


def info(message: str):
    _log('INFO', message, _GREEN)


def warn(message: str):
    _log('WARN', message, _YELLOW)


def error(message: str):
    _log('ERROR', message, _RED)


def fatal(message: str):
    _log('FATAL', message, _RED)


def _timestamp():
    t = time.time()
    lt = time.localtime(t)
    ms = int((t - int(t)) * 1000)
    return time.strftime('%Y-%m-%d %H:%M:%S', lt) + f'.{ms: 03d}'


def _log(level: str, message: str, color: str = None):
    if _log_file is None:
        raise RuntimeError(
            'Logger not initialized. Call reset() before logging.')
    if _LEVELS[level] < _log_level:
        return
    ts = _timestamp()
    line = f'{ts} [{level}] {message}'
    with open(_log_file, 'a') as f:
        f.write(line + '\n')
    if _console:
        if color:
            print(f'{color}{line}{_RESET}')
        else:
            print(line)
