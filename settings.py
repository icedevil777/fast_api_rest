import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Ylab Restaurant'
    database_url: str = os.getenv('DATABASE_URL', default='')


settings = Settings()

print('DATABASE_URL', settings.database_url)
