from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

#Find .env regardless of CWD
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
env_path = os.path.join(project_root, ".env")

class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    JWT_SECRET: str
    ALLOWED_DOMAINS: str

    max_upload_bytes: int = 5 * 1024 * 1024 #5MB

    model_config = SettingsConfigDict(
        env_file=env_path, 
        env_file_encoding="utf-8"
    )
    
    @property
    def allowed_domains_list(self) -> list[str]:
        return [d.strip() for d in self.ALLOWED_DOMAINS.split(",") if d.strip()]

@lru_cache
def get_settings():
    return Settings()
    