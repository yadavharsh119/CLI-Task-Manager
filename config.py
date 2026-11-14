import os
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "your current connection string",
)
