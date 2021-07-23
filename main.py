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


def configure_api_keys():
    file = Path('settings.json').absolute()
    if not file.exists():
        print(f"WARNING: {file} was not found, the api will not function, please see settings_template.json")
        raise Exception("settings.json file not found, please see settings_template.json")

    with open('settings.json') as infile:
        settings = json.load(infile)
        pass_service.api_key = settings.get('pass_api_key')
        n2sn_service.api_key = settings.get('n2snadmin_api_key')

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

