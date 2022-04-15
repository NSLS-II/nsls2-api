from typing import List

import fastapi

from models.instrument import Instrument
from services.pass_service import get_pass_resources_async
from infrastucture.database import fetch_all_beamlines

router = fastapi.APIRouter()

@router.get('/instruments')
async def get_instruments() -> List[Instrument]:
    response = await fetch_all_beamlines()
    return response


#@router.get('/instrument/{beamline}')
#def read_beamline(beamline: str):
#    # TODO: Validate beamline string is valid
#    return {"name": "TST"}

#@router.get('/instrument/{beamline}/{endstation}')
#async def instrument() -> List[Instrument]:
#    pass


#@router.get('/pass-resources')
async def get_pass_resources() -> List[Instrument]:
    resources = await get_pass_resources_async()
    return resources
