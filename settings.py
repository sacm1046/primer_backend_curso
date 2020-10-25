import os
from datetime import timedelta
# settings.py
from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
ENV = 'development'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db') 
SQLALCHEMY_TRACK_MODIFICATIONS = False

#JWT configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)