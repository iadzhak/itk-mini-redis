import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PORT: str = os.environ.get('PORT', '50051')
    MAX_WORKERS: int = int(os.environ.get('MAX_WORKERS', '0'))

    LRU_EVICTION: int = int(os.environ.get('LRU_EVICTION', '10'))

    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'info').upper()


settings = Settings()
