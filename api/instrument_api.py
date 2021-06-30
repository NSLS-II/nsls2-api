from typing import List

import fastapi

from models.instrument import Instrument

router = fastapi.APIRouter()


@router.get('/instrument/{instrument}')
def instrument() -> List[Instrument]:
    pass
