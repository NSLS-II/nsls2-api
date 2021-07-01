from typing import List

import fastapi

from models.instrument import Instrument

router = fastapi.APIRouter()

@router.get('/instruments')
def instrument() -> List[Instrument]:
    pass

@router.get('/instrument/{beamline}')
def instrument() -> List[Instrument]:
    pass

@router.get('/instrument/{beamline}/{endstation}')
def instrument() -> List[Instrument]:
    pass

