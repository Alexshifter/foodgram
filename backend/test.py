import os

from dotenv import load_dotenv
from foodgram_backend import settings
load_dotenv()

s = os.getenv('PG_EXIST')
print(s)
print(os.getenv('PG_EXIST', '').lower() == 'true')
print(settings.FIXTURE_DIRS)
print(settings.BASE_DIR)
DEBUG = (os.getenv('DEBUG_STATUS').lower() == 'true')
print(DEBUG)
#ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost, 127.0.0.1').split(', ')
print(ALLOWED_HOSTS)