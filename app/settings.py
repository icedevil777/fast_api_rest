import os
from pydantic import BaseSettings


class Settings(BaseSettings):
	app_title: str = 'Ylab Restaurant'
	database_url: str = os.getenv('DATABASE_URL', default='')
	# database_url: str = "postgresql+asyncpg://root:root@localhost:5432/root"

	class Config:
		env_file = ".env"


settings = Settings()

print('database_url:', settings.database_url)
