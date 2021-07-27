from typing import List

import fastapi

from models.instrument import Instrument

router = fastapi.APIRouter()

@router.get('/instruments')
def get_instruments() -> List[Instrument]:
    pass

@router.get('/instrument/{beamline}')
def read_beamline(beamline: str):
    # TODO: Validate beamline string is valid
    return {"name": "TST"}

@router.get('/instrument/{beamline}/{endstation}')
async def instrument() -> List[Instrument]:
    pass

