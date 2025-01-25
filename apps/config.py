from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRATON_MINUTES: int


    class Config:
        env_file = ".env"  # Load from a .env file (optional)

# Create an instance of Settings
settings = Settings()

