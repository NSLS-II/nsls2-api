from starlette.config import Config
from starlette.datastructures import URL, Secret, CommaSeparatedStrings

config = Config(".env-scripts")

DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)

ACTIVE_DIRECTORY_SERVER = config('ACTIVE_DIRECTORY_SERVER', cast=str)
ACTIVE_DIRECTORY_SERVER_LIST = config('ACTIVE_DIRECTORY_SERVER_LIST')
N2SN_USER_SEARCH = config('N2SN_USER_SEARCH')
N2SN_GROUP_SEARCH = config('N2SN_GROUP_SEARCH')
BNLROOT_CA_CERTS_FILE = config('BNLROOT_CA_CERTS_FILE', cast=str)
N2SN_CACHE_DB_CONNECTION = config('N2SN_CACHE_DB_CONNECTION', cast=str)
NSLS2CORE_MONGODB_URI = config('NSLS2CORE_MONGODB_URI', cast=str)
