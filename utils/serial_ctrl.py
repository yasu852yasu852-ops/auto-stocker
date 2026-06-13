import config
import time

try:
    import serial
except Exception:
    serial = None

class SerialController:
    def __init__(self, port=None, baud=None, timeout=1):
        self.port = port or config.SERIAL_PORT
        self.baud = baud or config.SERIAL_BAUD
        self.timeout = timeout
        self._conn = None
        self._mock = serial is None
        if self._mock:
            print('pyserial not installed or unavailable: running mock serial')

    def connect(self):
        if self._mock:
            return True
        try:
            self._conn = serial.Serial(self.port, self.baud, timeout=self.timeout)
            time.sleep(0.1)
            return True
        except Exception as e:
            print('Serial connect error:', e)
            return False

    def send(self, msg: str):
        payload = (msg + "\n").encode('utf-8')
        if self._mock:
            print('[SERIAL-MOCK] ->', msg)
            return True
        try:
            self._conn.write(payload)
            return True
        except Exception as e:
            print('Serial write error:', e)
            return False

    def close(self):
        if self._mock:
            return
        try:
            self._conn.close()
        except Exception:
            pass

serial_ctrl = SerialController()
