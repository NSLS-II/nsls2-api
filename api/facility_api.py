from typing import List

import fastapi
from pymongo import MongoClient

from fastapi.responses import JSONResponse

from infrastucture import settings
from models.facility import Facility, FacilityName

client = MongoClient(settings.NSLS2CORE_MONGODB_URI)
# client = motor.motor_asyncio.AsyncIOMotorClient(settings.NSLS2CORE_MONGODB_URI)


router = fastapi.APIRouter()

facility_data = {
    'nsls2': {'name': 'NSLS-II', 'id': 'nsls2', 'fullname': 'National Synchrotron Light Source II',
              'pass_facility_id': 'NSLS-II'},
    'lbms': {'name': 'LBMS', 'id': 'lbms', 'fullname': 'Laboratory for Biomolecular Structure',
             'pass_facility_id': 'LBMS'}
}
@router.get('/facility/{facility}/cycles/proposals')
async def get_facility_cycles_with_proposals(facility: FacilityName):
    database = client["nsls2core"]
    collection = database["cycles"]
    # Just return them all for the moment as we only have nsls2 cycles
    query = {"facility": str(facility.name)}
    projection = {"name": 1.0, "year": 1.0, "facility": 1.0, "active": 1.0, "proposals": 1.0, "_id": 0.0}
    cursor = collection.find(query, projection=projection)
    result = []
    for doc in cursor:
        result.append(doc)
    return result

@router.get('/facility/{facility}/cycles')
async def get_facility_cycles(facility: FacilityName):
    database = client["nsls2core"]
    collection = database["cycles"]
    # Just return them all for the moment as we only have nsls2 cycles
    query = {"facility": str(facility.name)}
    projection = {"name": 1.0, "year": 1.0, "facility": 1.0, "active": 0.0, "_id": 0.0}
    cursor = collection.find(query, projection=projection)
    result = []
    for doc in cursor:
        result.append(doc)
    return result

@router.get('/facility/{facility}', response_model=Facility)
def get_facility(facility: FacilityName):
    return facility_data[facility.name]


@router.get('/facilities', response_model=List[Facility])
def get_all_facilities():
    return list(facility_data.values())
