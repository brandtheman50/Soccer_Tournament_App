import environ
import os

env = environ.Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLIENT_HOSTNAME = env.str("CLIENT_HOSTNAME", default="http://localhost:3000")
API_HOSTNAME = env.str("API_HOSTNAME", default="http://localhost:8000")

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))