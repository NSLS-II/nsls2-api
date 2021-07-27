from typing import List

import fastapi

from services.pass_service import get_cycles_async
from models.facility import Facility

router = fastapi.APIRouter()




@router.get('/facility/{facility}/cycles')
async def get_facility_cycles(facility: str):
    cycles = await get_cycles_async()
    return cycles


@router.get('/facility/{facility}')
def get_facility():
    pass

@router.get('/facilities')
def get_all_facilities():
    pass