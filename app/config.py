import os

DATABASE_URL: str = os.getenv('DATABASE_URL_2')

SALT: str = os.getenv('SALT')
ALGORITHM: str = os.getenv('ALGORITHM')
TIMEOUT: int = int(os.getenv('TIMEOUT'))
