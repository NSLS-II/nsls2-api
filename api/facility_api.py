from typing import List

import fastapi

from models.facility import Facility

router = fastapi.APIRouter()

@router.get('/facilities')
def get_all_facilities():
    pass

@router.get('/facility/{facility}')
def get_facility():
    pass


