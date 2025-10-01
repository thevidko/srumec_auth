from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()