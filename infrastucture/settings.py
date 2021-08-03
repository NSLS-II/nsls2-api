from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)

PASS_API_KEY = config('PASS_API_KEY', cast=Secret)
PASS_TEST_API_KEY = config('PASS_TEST_API_KEY', cast=Secret)
PASS_API_URL = config('PASS_API_URL', cast=URL, default="https://passservices.bnl.gov/passapi")
PASS_TEST_API_URL = config('PASS_TEST_API_URL', cast=URL, default="https://passservicesdev.bnl.gov/passapi")

N2SNADMIN_API_KEY = config('N2SNADMIN_API_KEY', cast=Secret)

ACTIVE_DIRECTORY_SERVER = config('ACTIVE_DIRECTORY_SERVER', cast=str)
ACTIVE_DIRECTORY_SERVER_LIST = config('ACTIVE_DIRECTORY_SERVER_LIST')
N2SN_USER_SEARCH = config('N2SN_USER_SEARCH')
N2SN_GROUP_SEARCH = config('N2SN_GROUP_SEARCH')
BNLROOT_CA_CERTS_FILE = config('BNLROOT_CA_CERTS_FILE', cast=str)

if TESTING:
    PASS_API_KEY = PASS_TEST_API_KEY
    PASS_API_URL = PASS_TEST_API_URL

