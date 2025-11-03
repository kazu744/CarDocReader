import os
from dotenv import load_dotenv

load_dotenv()
print("DEBUG: FERNET_KEY in settings =", os.getenv("FERNET_KEY"))

SECRET_KEY = os.getenv('SECRET_KEY')
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("FERNET_KEY が読み込めてません。")

DB_DIALECT = os.getenv('DB_DIALECT')
DB_DRIVER = os.getenv('DB_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASSWD = os.getenv('DB_PASSWD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')