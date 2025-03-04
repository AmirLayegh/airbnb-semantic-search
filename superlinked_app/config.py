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
    
    DATA_PATH: str = "/Users/amlk/MLOps-training/listings.csv"
    USE_QDRANT_VECTOR_DB: bool = True
    QDRANT_CLUSTER_NAME: str = 'airbnb'
    QDRANT_COLLECTION_NAME: str = 'airbnb_semantic_search'
    QDRANT_API_KEY: SecretStr
    QDRANT_CLUSTER_URL: SecretStr
    
    OPENAI_API_KEY: SecretStr
    OPENAI_MODEL_ID: str = "gpt-4o"

    @model_validator(mode='after')
    def validate_qdrant_config(self) -> "Settings":
        if self.USE_QDRANT_VECTOR_DB:
            required_settings = [
                "QDRANT_CLUSTER_URL",
                "QDRANT_API_KEY",
                "QDRANT_CLUSTER_NAME",
                "QDRANT_COLLECTION_NAME",
            ]
            
            missing_settings = [
            setting for setting in required_settings 
            if not getattr(self, setting, None)
        ]
        
        if missing_settings:
            raise ValueError(f"Missing required Qdrant settings: {missing_settings}")
        
        return self
    
    
setting = Settings()