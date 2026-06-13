import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost:5432/auto_stocker')
SERIAL_PORT = os.getenv('SERIAL_PORT', '/dev/ttyUSB_STK')
SERIAL_BAUD = int(os.getenv('SERIAL_BAUD', '115200'))
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')

# Application settings
IS_SYSTEM_BUSY_TIMEOUT = 5  # seconds demo lock
