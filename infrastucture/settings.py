from starlette.config import Config
from starlette.datastructures import URL, Secret

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)

PASS_API_KEY = config('PASS_API_KEY', cast=Secret)
PASS_TEST_API_KEY = config('PASS_TEST_API_KEY', cast=Secret)
PASS_API_URL = config('PASS_API_URL', cast=URL, default="https://passservices.bnl.gov/passapi")
PASS_TEST_API_URL = config('PASS_TEST_API_URL', cast=URL, default="https://passservicesdev.bnl.gov/passapi")

N2SNADMIN_API_KEY = config('N2SNADMIN_API_KEY', cast=Secret)

if TESTING:
    PASS_API_KEY = PASS_TEST_API_KEY
    PASS_API_URL = PASS_TEST_API_URL
