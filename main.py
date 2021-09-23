import json
from pathlib import Path
import time

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles
from fastapi import Request

from api import instrument_api
from api import facility_api
from api import proposal_api
from api import users_api

from infrastucture import settings

from services import pass_service
from services import n2sn_service
from views import home

api = fastapi.FastAPI()
#api = fastapi.FastAPI(root_path="/api")


@api.middleware("http")
async def add_server_timing_header(request: Request, call_next):
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server-Timing
    # https://w3c.github.io/server-timing/#the-server-timing-header-field
    # This information seems safe to share because the user can easily
    # estimate it based on request/response time, but if we add more detailed
    # information here we should keep in mind security concerns and perhaps
    # only include this for certain users.
    # Units are ms.
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["Server-Timing"] = f"app;dur={1000 * process_time:.1f}"
    return response

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

