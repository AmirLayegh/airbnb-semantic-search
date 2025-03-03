from pathlib import Path

from loguru import logger
from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent
ENV_FILE = ROOT_DIR / ".env"
logger.info("Loading environment variables from .env file: %s", ENV_FILE)

assert ENV_FILE.exists(), f"Environment file not found: {ENV_FILE}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), env_file_encoding="utf-8")
    
    OPENAI_API_KEY: SecretStr
    OPENAI_MODEL_ID: str = "gpt-4o"
    
    
setting = Settings()