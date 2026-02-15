from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    DB_HOST : str
    DB_PORT : int 
    DB_USER : str
    DB_PASS : str
    DB_NAME : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRES_MINUTES : int
    REFRESH_TOKEN_EXPIRES_DAYS : int


    @property
    def DATABSE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    redis_host: str = Field(default="localhost", validation_alias="REDIS_HOST")
    redis_port: int = Field(default=6379, validation_alias="REDIS_PORT")
    redis_db: int = Field(default=0, validation_alias="REDIS_DB")

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")


settings = Settings()