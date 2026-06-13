import time
import threading

_lock = threading.Lock()
_is_busy = False
_busy_until = 0
TIMEOUT = 5

def acquire():
    global _is_busy, _busy_until
    with _lock:
        now = time.time()
        if _is_busy and now < _busy_until:
            return False
        _is_busy = True
        _busy_until = now + TIMEOUT
        return True

def release():
    global _is_busy, _busy_until
    with _lock:
        _is_busy = False
        _busy_until = 0

def is_busy():
    return _is_busy and time.time() < _busy_until
