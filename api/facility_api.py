from typing import List

import fastapi

from services.pass_service import get_cycles_async
from models.facility import Facility, FacilityName

router = fastapi.APIRouter()

facility_data = {
    'nsls2': {'name': 'NSLS-II', 'id': 'nsls2', 'fullname': 'National Synchrotron Light Source II', 'pass_facility_id': 'NSLS-II'},
    'lbms': {'name': 'LBMS', 'id': 'lbms', 'fullname': '', 'pass_facility_id': 'LBMS'}
}


@router.get('/facility/{facility}/cycles')
async def get_facility_cycles(facility: FacilityName):
    cycles = await get_cycles_async()
    return cycles


@router.get('/facility/{facility}')
def get_facility(facility: FacilityName):
    return facility_data[facility.name]


@router.get('/facilities', response_model=Facility)
def get_all_facilities():
    return facility_data

