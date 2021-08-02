from enum import Enum
from typing import Optional, List

from pydantic.main import BaseModel

class FacilityName(Enum):
    nsls2="NSLS-II"
    lbms="LBMS"

class Facility(BaseModel):
    name: str
    fullname: str
    pass_facility_id: str

