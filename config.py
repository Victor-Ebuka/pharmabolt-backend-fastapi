import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection URL (PostgreSQL in this case)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost:5432/lms_db")

# JWT secret key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "my_secret_key")
