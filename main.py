import json
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from api import instrument_api
from api import facility_api
from api import proposal_api
from api import users_api

from infrastucture import settings

from services import pass_service
from services import n2sn_service
from views import home

api = fastapi.FastAPI()

def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(instrument_api.router)
    api.include_router(facility_api.router)
    api.include_router(proposal_api.router)
    api.include_router(users_api.router)

def configure():
    configure_routing()

if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()

