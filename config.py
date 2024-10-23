from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Technia Task"
    app_port: int = 8005
    app_path: str = ""
    auth_url: str = "http://localhost:8005"
    database_host: str = ""
    database_username: str = ""
    database_password: str = ""
    database_name: str = ""
    database_type: str = ""
    environment: str = "development"
    profiling_enabled: bool = False
    profiling_dir: str = "profile"
    # email_host: str = ""
    # email_port: int = 465
    # email_username: str = ""
    # email_password: str = ""
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings(_env_file=".env")


settings = get_settings()
