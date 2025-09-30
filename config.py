import os

class Config:
    DB_HOST = 'nzgz3x.h.filess.io'
    DB_USER = 'Angel2_justladyas'
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = 'Angel2_justladyas'
    DB_PORT = 5432
    
    @staticmethod
    def get_db_uri():
        return f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
