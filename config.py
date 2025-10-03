import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = 'nzgz3x.h.filess.io'
    DB_USER = 'Angel2_justladyas'
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = 'Angel2_justladyas'
    DB_PORT = 3306
    DB_CHARSET = 'utf8mb4'
