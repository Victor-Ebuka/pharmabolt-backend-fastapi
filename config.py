import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Database connection URL (PostgreSQL in this case)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

# JWT secret key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_secret_key")

# Access token expiration time (in seconds)
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

# Algorithm for password hashing
ALGORITHM = os.getenv("ALGORITHM", "HS256")

