import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")
    BACKEND_API_URL = os.getenv("BACKEND_SERVER_ENDPOINT")

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))


settings = Settings()
