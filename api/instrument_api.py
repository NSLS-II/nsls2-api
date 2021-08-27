from typing import List

import fastapi

from models.instrument import Instrument
from services.pass_service import get_pass_resources_async

router = fastapi.APIRouter()

@router.get('/instruments')
async def get_instruments() -> List[Instrument]:
    resources = await get_pass_resources_async()
    return resources

@router.get('/instrument/{beamline}')
def read_beamline(beamline: str):
    # TODO: Validate beamline string is valid
    return {"name": "TST"}

@router.get('/instrument/{beamline}/{endstation}')
async def instrument() -> List[Instrument]:
    pass

