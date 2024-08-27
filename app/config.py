import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
# Retrieve the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Secret key for JWT
# In production, this should be set as an environment variable
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
if SECRET_KEY == "your-secret-key":
    print("Warning: Using default SECRET_KEY. This is insecure in production.")

# JWT algorithm
ALGORITHM = "HS256"

# Other config variables can be added here