# logger.py

DEBUG = True  # flip to False to silence debug output

def _prefix(level):
    return "[{}]".format(level)

def debug(msg):
    if DEBUG:
        print(f"{_prefix('DBG')} {msg}")

def info(msg):
    print(f"{_prefix('INF')} {msg}")

def warn(msg):
    print(f"{_prefix('WRN')} {msg}")

def error(msg):
    print(f"{_prefix('ERR')} {msg}")
