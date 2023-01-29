import os
from pydantic import BaseSettings


class Settings(BaseSettings):
	app_title: str = 'Ylab Restaurant'
	_env_file = '.env'
	_env_file_encoding = 'utf-8'
	# database_url: str = os.getenv('DATABASE_URL', default='')
	database_url: str = "postgresql+asyncpg://root:root@localhost:5432/root"


settings = Settings()

print('database_url:', settings.database_url)
